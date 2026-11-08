"""Print historical stats, and optionally the named strategies, for the sample data."""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from portfolio_lab.analysis import analyse
from portfolio_lab.data import list_assets, aligned_prices
from portfolio_lab.returns import TRADING_DAYS, annualize_mean, simple_returns_matrix
from portfolio_lab.risk import sample_covariance
from portfolio_lab.stats import best_worst_month, max_drawdown, sharpe_ratio


def _asset_table(market: str, window: str, risk_free: float) -> None:
    assets = list_assets(market)
    tickers = [asset["ticker"] for asset in assets]
    prices, metas, note = aligned_prices(market, tickers, window)
    returns = simple_returns_matrix(prices.to_numpy(dtype=float))
    dates = prices.index[1:]
    covariance = sample_covariance(returns) * TRADING_DAYS
    volatility = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    means = annualize_mean(returns.mean(axis=0))
    print(f"Portfolio Lab - {market}, window {window} ({len(returns)} daily returns)")
    print("Returns are simple price returns, annualised x 252. Sample covariance uses n - 1.")
    if note:
        print(note)
    print()
    header = f"{'Ticker':<10} {'Return':>8} {'Vol':>8} {'Sharpe':>8} {'Max DD':>8} {'Best month':>18} {'Worst month':>18} {'Dividend':>10}"
    print(header)
    for index, meta in enumerate(metas):
        series = pd.Series(returns[:, index], index=pd.DatetimeIndex(dates))
        months = best_worst_month(series)
        sharpe = sharpe_ratio(float(means[index]), float(volatility[index]), risk_free)
        dividend = meta.get("dividend_yield")
        best = _month(months["best"])
        worst = _month(months["worst"])
        print(
            f"{meta['ticker']:<10} {means[index]:>8.1%} {volatility[index]:>8.1%} "
            f"{_maybe(sharpe):>8} {max_drawdown(returns[:, index]):>8.1%} {best:>18} {worst:>18} {_yield(dividend):>10}"
        )


def _month(entry: dict | None) -> str:
    if not entry:
        return "-"
    return f"{entry['label']} {entry['return']:+.1%}"


def _maybe(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.2f}"


def _yield(value) -> str:
    if value is None:
        return "n/a"
    return f"{value:.1%}"


def _strategies(market: str, window: str, tickers: list[str], risk_free: float, cap: float, cash_yield: float) -> None:
    result = analyse(
        {
            "market": market,
            "tickers": tickers,
            "weights": {},
            "strategy": "equal",
            "window": window,
            "risk_free_rate": risk_free,
            "max_weight": cap,
            "include_cash": True,
            "cash_yield": cash_yield,
            "cash_weight": None,
            "expected_return_overrides": {},
        }
    )
    print()
    print(f"Strategies for {', '.join(tickers)} plus cash. Cap {cap:.0%}. Cash yield {cash_yield:.1%}.")
    print("Your weights are blank here, so that row may be infeasible until you type weights in the app.")
    print()
    for row in result["comparison"]:
        if not row.get("ok"):
            print(f"{row['name']}: {row['error']}")
            continue
        mix = ", ".join(f"{item['ticker']} {item['weight']:.1%}" for item in row["weights"])
        sharpe = row["objective_sharpe"]
        sharpe_text = "undefined" if sharpe is None else f"{sharpe:.2f}"
        print(
            f"{row['name']}: vol {row['volatility']:.1%}, expected {row['expected_return']:.1%}, "
            f"Sharpe {sharpe_text}"
        )
        print(f"  {mix}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Print sample-universe stats for Portfolio Lab.")
    parser.add_argument("--market", default="US", choices=["US", "UK"])
    parser.add_argument("--window", default="1y", choices=["1y", "3y", "5y", "all"])
    parser.add_argument("--rf", type=float, default=0.04)
    parser.add_argument("--cap", type=float, default=0.40)
    parser.add_argument("--cash-yield", type=float, default=0.04)
    parser.add_argument("--tickers", default="", help="Comma-separated tickers. When set, also print strategies.")
    args = parser.parse_args(argv)
    _asset_table(args.market, args.window, args.rf)
    tickers = [part.strip() for part in args.tickers.split(",") if part.strip()]
    if tickers:
        _strategies(args.market, args.window, tickers, args.rf, args.cap, args.cash_yield)


if __name__ == "__main__":
    main()
