"""Simple returns and the 252-day annualisation used everywhere in the app."""

from __future__ import annotations

import numpy as np

TRADING_DAYS = 252


def simple_returns_matrix(prices: np.ndarray) -> np.ndarray:
    """Percent change down each column. `prices` is shaped (days, assets)."""
    values = np.asarray(prices, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2:
        raise ValueError("Need at least two prices to compute a return.")
    previous = values[:-1]
    if np.any(previous <= 0) or not np.isfinite(values).all():
        raise ValueError("Prices must be finite and above zero.")
    return values[1:] / previous - 1.0


def annualize_mean(daily_mean: np.ndarray) -> np.ndarray:
    """Arithmetic annualisation: multiply the average daily return by 252."""
    return np.asarray(daily_mean, dtype=float) * TRADING_DAYS


def annualize_covariance(daily_covariance: np.ndarray) -> np.ndarray:
    """Annualise a daily covariance matrix by multiplying every entry by 252."""
    return np.asarray(daily_covariance, dtype=float) * TRADING_DAYS
