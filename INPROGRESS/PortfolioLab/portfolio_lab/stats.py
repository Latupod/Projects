"""Sharpe, drawdown, and best/worst month.

Drawdown and the best/worst month use a constant-mix path: the same weights
applied every day, as if the portfolio were put back to those weights each day.
That is not a backtest with trading costs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

_VOL_FLOOR = 1e-12


def sharpe_ratio(annual_return: float, annual_volatility: float, risk_free_rate: float) -> float | None:
    """(return − risk-free rate) / volatility. Undefined when volatility is zero."""
    if annual_volatility is None or not np.isfinite(annual_volatility) or annual_volatility < _VOL_FLOOR:
        return None
    return float((annual_return - risk_free_rate) / annual_volatility)


def constant_mix_returns(asset_returns: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """One portfolio return per day: each day is the weighted sum of asset returns."""
    returns = np.asarray(asset_returns, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if returns.ndim != 2 or returns.shape[1] != weights.shape[0]:
        raise ValueError("Weights must match the number of return columns.")
    return returns @ weights


def wealth_path(returns: np.ndarray) -> np.ndarray:
    """Growth of 1 unit of currency, including the starting value of 1."""
    values = np.asarray(returns, dtype=float)
    return np.concatenate([[1.0], np.cumprod(1.0 + values)])


def drawdown_path(returns: np.ndarray) -> np.ndarray:
    """Drawdown at each point on the wealth path, starting at 0. Values are ≤ 0."""
    wealth = wealth_path(returns)
    peak = np.maximum.accumulate(wealth)
    return wealth / peak - 1.0


def max_drawdown(returns: np.ndarray) -> float:
    """Largest peak-to-trough loss, as a positive fraction (0.12 means a 12% fall)."""
    path = drawdown_path(returns)
    return float(-np.min(path))


def monthly_simple_returns(daily_returns: pd.Series) -> pd.Series:
    """Compound daily simple returns into calendar months."""
    if daily_returns.empty:
        return daily_returns
    return (1.0 + daily_returns).resample("ME").prod() - 1.0


def best_worst_month(daily_returns: pd.Series) -> dict:
    """Best and worst calendar month. Either side can be None on an empty series."""
    monthly = monthly_simple_returns(daily_returns)
    monthly = monthly.replace([np.inf, -np.inf], np.nan).dropna()
    if monthly.empty:
        return {"best": None, "worst": None}
    best_at = monthly.idxmax()
    worst_at = monthly.idxmin()
    return {
        "best": {"label": best_at.strftime("%Y-%m"), "return": float(monthly.loc[best_at])},
        "worst": {"label": worst_at.strftime("%Y-%m"), "return": float(monthly.loc[worst_at])},
    }
