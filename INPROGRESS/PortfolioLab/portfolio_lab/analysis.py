"""Turn a portfolio request into stats, matrices, strategies, and chart series."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from portfolio_lab.data import CASH_NAME, CASH_TICKER, aligned_prices, market_info, resolve_prices
from portfolio_lab.optimize import (
    InfeasibleError,
    equal_weight,
    efficient_frontier,
    maximum_sharpe,
    minimum_variance,
    standard_bounds,
    user_weights,
)
from portfolio_lab.returns import TRADING_DAYS, annualize_covariance, annualize_mean, simple_returns_matrix
from portfolio_lab.risk import (
    component_risk,
    correlation_from_covariance,
    portfolio_variance,
    portfolio_volatility,
    sample_covariance,
    sigma_times_weights,
)
from portfolio_lab.stats import best_worst_month, constant_mix_returns, drawdown_path, max_drawdown, sharpe_ratio, wealth_path

STRATEGIES = (
    ("user", "Your weights"),
    ("equal", "Equal weight"),
    ("min_variance", "Cautious (minimum variance)"),
    ("max_sharpe", "Balanced (maximum Sharpe)"),
    ("growth", "Growth"),
)
MAX_HOLDINGS = 12


def analyse(spec: dict) -> dict:
    """Build the full teaching payload for one portfolio specification."""
    market = spec.get("market")
    info = market_info(market)
    tickers = _unique_tickers(spec.get("tickers") or [])
    if not tickers:
        raise ValueError("Select at least one stock or ETF. Cash can be added beside it.")
    if len(tickers) > MAX_HOLDINGS:
        raise ValueError("Choose 12 holdings or fewer so the covariance matrix stays readable.")
    window = spec.get("window", "3y")
    risk_free = _rate("The risk-free rate", spec.get("risk_free_rate", 0.04))
    max_weight = float(spec.get("max_weight", 0.40))
    include_cash = bool(spec.get("include_cash", False))
    cash_yield = _rate("The cash yield", spec.get("cash_yield", 0.04)) if include_cash else 0.0
    locked_cash = spec.get("cash_weight", None)
    if locked_cash is not None and locked_cash != "":
        locked_cash = _rate("The locked cash weight", locked_cash)
    else:
        locked_cash = None
    strategy = spec.get("strategy", "user")
    if strategy not in {key for key, _ in STRATEGIES}:
        raise ValueError("Unknown strategy.")
    overrides = _overrides(spec.get("expected_return_overrides") or {}, tickers)

    prices, metas, window_note = aligned_prices(market, tickers, window)
    dates = prices.index[1:]
    returns = simple_returns_matrix(prices.to_numpy(dtype=float))
    mask = np.isfinite(returns).all(axis=1)
    returns = returns[mask]
    dates = dates[mask]
    if len(returns) < 2:
        raise ValueError("Not enough overlapping prices in this window to estimate a covariance matrix.")

    daily_cov = sample_covariance(returns)
    annual_cov = annualize_covariance(daily_cov)
    historical_means = annualize_mean(returns.mean(axis=0))
    names = [meta["name"] for meta in metas]

    if include_cash:
        tickers = tickers + [CASH_TICKER]
        names = names + [CASH_NAME]
        metas = metas + [{"ticker": CASH_TICKER, "name": CASH_NAME, "kind": "cash", "dividend_yield": None}]
        size = annual_cov.shape[0]
        expanded = np.zeros((size + 1, size + 1))
        expanded[:size, :size] = annual_cov
        annual_cov = expanded
        historical_means = np.append(historical_means, cash_yield)
        cash_daily = np.full((len(returns), 1), cash_yield / TRADING_DAYS)
        returns = np.concatenate([returns, cash_daily], axis=1)

    expected_means = historical_means.copy()
    for ticker, value in overrides.items():
        expected_means[tickers.index(ticker)] = value

    cash_index = tickers.index(CASH_TICKER) if include_cash else None
    base_bounds = standard_bounds(len(tickers), max_weight, cash_index=cash_index, growth=False)
    growth_bounds = standard_bounds(len(tickers), max_weight, cash_index=cash_index, growth=True)

    raw_user = _raw_user_weights(spec, tickers, include_cash, locked_cash)
    solved = {
        "user": lambda: user_weights(raw_user, base_bounds),
        "equal": lambda: (equal_weight(base_bounds, cash_index, locked_cash if include_cash else None), False),
        "min_variance": lambda: (minimum_variance(annual_cov, base_bounds), False),
        "max_sharpe": lambda: (maximum_sharpe(expected_means, annual_cov, risk_free, base_bounds), False),
        "growth": lambda: (maximum_sharpe(expected_means, annual_cov, risk_free, growth_bounds), False),
    }

    comparison = []
    solved_weights: dict[str, np.ndarray] = {}
    for key, label in STRATEGIES:
        try:
            weights, scaled = solved[key]()
            solved_weights[key] = weights
            comparison.append(
                _strategy_row(
                    key, label, weights, scaled, returns, dates, annual_cov, historical_means, expected_means, risk_free, tickers
                )
            )
        except InfeasibleError as exc:
            comparison.append({"key": key, "name": label, "ok": False, "error": str(exc)})

    active = next(row for row in comparison if row["key"] == strategy)
    warning = _sample_warning(len(returns), len(tickers) - (1 if include_cash else 0))
    payload = {
        "ok": bool(active.get("ok")),
        "error": active.get("error"),
        "market": market,
        "currency": info["currency"],
        "currency_label": info["currency_label"],
        "benchmark": info["benchmark"],
        "window": window,
        "window_note": window_note,
        "warning": warning,
        "risk_free_rate": risk_free,
        "max_weight": float(max_weight),
        "include_cash": include_cash,
        "cash_yield": cash_yield if include_cash else None,
        "observations": int(len(returns)),
        "annualization_note": (
            "Means and covariances are annualised by multiplying the daily sample estimates by 252. "
            "Covariance uses the sample formula, dividing by the number of days minus one."
        ),
        "dividend_note": (
            "Historical returns are price changes only. Dividend yield is shown beside them when the "
            "file has it, and it is not added into the return."
        ),
        "comparison": comparison,
        "captions": {},
    }
    if not active.get("ok"):
        payload["captions"] = {
            "error": active["error"],
        }
        return payload

    weights = solved_weights[strategy]
    math_block = _math_block(tickers, names, weights, annual_cov)
    asset_stats = _asset_stats(tickers, metas, weights, returns, dates, annual_cov, historical_means, expected_means, risk_free, math_block)
    portfolio_stats = _portfolio_stats(
        weights, returns, dates, annual_cov, historical_means, expected_means, risk_free, active.get("weights_were_scaled", False)
    )
    charts = _charts(
        market, info, tickers, names, dates, returns, weights, expected_means, annual_cov, base_bounds, comparison
    )
    payload.update(
        {
            "math": math_block,
            "assets": asset_stats,
            "portfolio": portfolio_stats,
            "charts": charts,
            "captions": _captions(portfolio_stats, math_block, include_cash, strategy, warning),
        }
    )
    return payload


def _unique_tickers(tickers: list) -> list[str]:
    chosen = []
    for ticker in tickers:
        text = str(ticker).strip()
        if text and text != CASH_TICKER and text not in chosen:
            chosen.append(text)
    return chosen


def _rate(name: str, value) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a number.") from exc
    if not math.isfinite(number) or not -0.2 <= number <= 1:
        raise ValueError(f"{name} must be between -20% and 100%.")
    return number


def _overrides(raw: dict, tickers: list[str]) -> dict[str, float]:
    if not isinstance(raw, dict):
        raise ValueError("Expected-return overrides must be an object of ticker to return.")
    cleaned = {}
    for ticker, value in raw.items():
        if value is None or value == "":
            continue
        text = str(ticker)
        if text == CASH_TICKER:
            continue
        if text not in tickers:
            raise ValueError(f"Cannot override {text} because it is not in the portfolio.")
        cleaned[text] = _rate(f"The expected return for {text}", value)
    return cleaned


def _raw_user_weights(spec: dict, tickers: list[str], include_cash: bool, locked_cash: float | None) -> np.ndarray:
    typed = spec.get("weights") or {}
    if not isinstance(typed, dict):
        raise ValueError("Weights must be an object of ticker to weight.")
    weights = []
    for ticker in tickers:
        if ticker == CASH_TICKER:
            value = locked_cash if locked_cash is not None else 0.0
        else:
            value = typed.get(ticker, 0.0)
        try:
            weights.append(float(value))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"The weight for {ticker} must be a number.") from exc
    return np.array(weights, dtype=float)


def _sample_warning(n_observations: int, n_risky: int) -> str | None:
    if n_observations < 60 or n_observations < 10 * max(n_risky, 1):
        return (
            f"This window has {n_observations} daily returns and {n_risky} risky holdings. "
            "A covariance matrix estimated from a short window is noisy, so the risk figures "
            "can jump around if you change the dates."
        )
    return None


def _math_block(tickers, names, weights, covariance) -> dict:
    sigma_w = sigma_times_weights(weights, covariance)
    variance = portfolio_variance(weights, covariance)
    volatility = portfolio_volatility(weights, covariance)
    components = component_risk(weights, covariance)
    if volatility < 1e-18:
        shares = [None] * len(tickers)
    else:
        shares = [float(component / volatility) for component in components]
    correlation = correlation_from_covariance(covariance)
    return {
        "tickers": tickers,
        "names": names,
        "weights": [float(weight) for weight in weights],
        "covariance": _matrix(covariance),
        "correlation": _matrix(correlation),
        "sigma_w": [float(value) for value in sigma_w],
        "variance": float(variance),
        "volatility": float(volatility),
        "component_risk": [float(value) for value in components],
        "component_share": shares,
        "negative_component": bool(np.any(components < -1e-8)),
        "zero_risk": bool(volatility < 1e-12),
    }


def _strategy_row(key, label, weights, scaled, returns, dates, covariance, historical_means, expected_means, risk_free, tickers):
    variance = portfolio_variance(weights, covariance)
    volatility = portfolio_volatility(weights, covariance)
    expected_return = float(weights @ expected_means)
    path = constant_mix_returns(returns, weights)
    historical_return = float(annualize_mean(path.mean()))
    return {
        "key": key,
        "name": label,
        "ok": True,
        "weights_were_scaled": bool(scaled),
        "weights": [{"ticker": ticker, "weight": float(weight)} for ticker, weight in zip(tickers, weights)],
        "expected_return": expected_return,
        "historical_return": historical_return,
        "volatility": float(volatility),
        "variance": float(variance),
        "objective_sharpe": sharpe_ratio(expected_return, volatility, risk_free),
        "historical_sharpe": sharpe_ratio(historical_return, volatility, risk_free),
    }


def _asset_stats(tickers, metas, weights, returns, dates, covariance, historical_means, expected_means, risk_free, math_block):
    stats = []
    vol = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    for index, ticker in enumerate(tickers):
        series = pd.Series(returns[:, index], index=pd.DatetimeIndex(dates))
        historical = float(historical_means[index])
        volatility = float(vol[index])
        dividend = metas[index].get("dividend_yield")
        stats.append(
            {
                "ticker": ticker,
                "name": metas[index].get("name", ticker),
                "kind": metas[index].get("kind", "stock"),
                "weight": float(weights[index]),
                "historical_return": historical,
                "expected_return": float(expected_means[index]),
                "volatility": volatility,
                "sharpe": sharpe_ratio(historical, volatility, risk_free),
                "max_drawdown": max_drawdown(returns[:, index]),
                "best_month": best_worst_month(series)["best"],
                "worst_month": best_worst_month(series)["worst"],
                "dividend_yield": None if dividend is None else float(dividend),
                "component_risk": math_block["component_risk"][index],
                "component_share": math_block["component_share"][index],
            }
        )
    return stats


def _portfolio_stats(weights, returns, dates, covariance, historical_means, expected_means, risk_free, scaled):
    path = constant_mix_returns(returns, weights)
    series = pd.Series(path, index=pd.DatetimeIndex(dates))
    months = best_worst_month(series)
    volatility = portfolio_volatility(weights, covariance)
    historical_return = float(annualize_mean(path.mean()))
    expected_return = float(weights @ expected_means)
    return {
        "historical_return": historical_return,
        "expected_return": expected_return,
        "volatility": float(volatility),
        "variance": portfolio_variance(weights, covariance),
        "historical_sharpe": sharpe_ratio(historical_return, volatility, risk_free),
        "objective_sharpe": sharpe_ratio(expected_return, volatility, risk_free),
        "max_drawdown": max_drawdown(path),
        "best_month": months["best"],
        "worst_month": months["worst"],
        "risk_free_rate": risk_free,
        "weights_were_scaled": bool(scaled),
    }


def _charts(market, info, tickers, names, dates, returns, weights, expected_means, covariance, bounds, comparison):
    path = constant_mix_returns(returns, weights)
    growth = {"portfolio": _growth_series(path)}
    asset_growth = {}
    for index, ticker in enumerate(tickers):
        if ticker == CASH_TICKER:
            continue
        asset_growth[ticker] = _growth_series(returns[:, index])
    growth["assets"] = asset_growth
    benchmark = _benchmark_growth(market, info["benchmark"]["ticker"], dates)
    frontier = []
    try:
        for point in efficient_frontier(expected_means, covariance, bounds):
            frontier.append(
                {
                    "expected_return": point["expected_return"],
                    "volatility": point["volatility"],
                }
            )
    except InfeasibleError:
        frontier = []
    points = []
    for row in comparison:
        if not row.get("ok"):
            continue
        points.append(
            {
                "key": row["key"],
                "name": row["name"],
                "expected_return": row["expected_return"],
                "volatility": row["volatility"],
            }
        )
    return {
        "dates": [pd.Timestamp(day).strftime("%Y-%m-%d") for day in dates],
        "names": names,
        "tickers": tickers,
        "growth": {**growth, "benchmark": benchmark, "benchmark_name": info["benchmark"]["name"]},
        "drawdown": _series(drawdown_path(path)[1:]),
        "frontier": frontier,
        "strategy_points": points,
    }


def _benchmark_growth(market: str, ticker: str, dates: pd.DatetimeIndex) -> list[float] | None:
    try:
        prices, _meta = resolve_prices(market, ticker)
    except LookupError:
        return None
    full = prices.sort_index().pct_change()
    common = full.reindex(pd.DatetimeIndex(dates))
    if common.isna().mean() > 0.1:
        return None
    return _growth_series(common.fillna(0.0).to_numpy())


def _growth_series(returns: np.ndarray) -> list[float]:
    """Cumulative growth rebased to 1 on the first date of the chart."""
    levels = wealth_path(np.asarray(returns, dtype=float))[1:]
    if len(levels) == 0 or levels[0] == 0:
        return []
    return _series(levels / levels[0])


def _captions(stats: dict, math_block: dict, include_cash: bool, strategy: str, warning: str | None) -> dict:
    volatility = stats["volatility"]
    captions = {
        "volatility": (
            f"Portfolio volatility is {volatility:.1%} a year. "
            "That is the square root of wᵀ Σ w: a typical yearly swing estimated from this window, not a forecast."
        ),
        "variance": (
            f"Variance is {stats['variance']:.6f}, which is w transpose times Σ times w. "
            "Volatility is the square root of this number."
        ),
        "sharpe": (
            "Sharpe divides return above your risk-free rate by volatility. "
            "A higher number is more historical return per unit of swing. It is not a recommendation to buy."
        ),
        "drawdown": (
            f"The largest peak-to-trough fall on the constant-mix path is {stats['max_drawdown']:.1%}. "
            "The path pretends the mix was put back to these weights every day. It does not include trading costs."
        ),
        "expected": (
            "Expected return starts as the annualised historical average. "
            "An override changes Balanced and Growth, and it does not change the covariance matrix."
        ),
        "allocation": "Each slice is the weight of that holding. The weights add up to 100%.",
        "frontier": (
            "Each point is the lowest-volatility mix that hits that expected return, under the same cap. "
            "Growth can sit inside the curve because it also limits cash to 10%."
        ),
    }
    cash_component = None
    if include_cash and CASH_TICKER in math_block["tickers"]:
        cash_at = math_block["tickers"].index(CASH_TICKER)
        cash_component = math_block["component_risk"][cash_at]
        if math_block["weights"][cash_at] > 0.01 and abs(cash_component) < 1e-8:
            captions["cash_risk"] = (
                "Cash has a weight but a zero slice of the risk chart, because this model gives cash "
                "no variance and no covariance. It lowers portfolio volatility by taking weight away from the risky holdings."
            )
    if math_block["zero_risk"]:
        captions["risk"] = (
            "Portfolio volatility is zero, so there is no risk to split. "
            "That happens when the mix is entirely cash or another zero-volatility holding."
        )
    elif math_block["negative_component"]:
        captions["risk"] = (
            "One holding has a negative component risk, so it is hedging the rest. "
            "A pie chart cannot show a negative slice, so the chart is a bar chart. "
            "The bars still add up to portfolio volatility."
        )
    else:
        captions["risk"] = (
            "Each slice is that holding's share of portfolio volatility. "
            "A slice can be smaller than the holding's weight when it diversifies the rest. "
            "The slices add up to 100% of portfolio volatility."
        )
    if stats["weights_were_scaled"]:
        captions["scaled"] = "Your weights did not add up to 100%, so they were scaled to 100% before scoring."
    if include_cash and strategy == "user":
        captions["cash"] = (
            "Cash is a synthetic holding: its yield is the number you typed, and its variance and covariances are zero. "
            "A blank cash weight is scored as 0%."
        )
    elif include_cash:
        captions["cash"] = (
            "Cash is a synthetic holding: its yield is the number you typed, and its variance and covariances are zero. "
            "Cautious can put a large share in cash because that lowers portfolio variance."
        )
    if strategy == "growth":
        captions["growth"] = "Growth is maximum Sharpe with cash held to 10% or less. Without cash, Growth matches Balanced."
    if warning:
        captions["warning"] = warning
    return captions


def _matrix(values: np.ndarray) -> list[list[float | None]]:
    rows = []
    for row in np.asarray(values, dtype=float):
        cleaned = []
        for value in row:
            if value is None or not math.isfinite(float(value)):
                cleaned.append(None)
            else:
                cleaned.append(float(value))
        rows.append(cleaned)
    return rows


def _series(values: np.ndarray) -> list[float]:
    return [float(value) for value in np.asarray(values, dtype=float)]
