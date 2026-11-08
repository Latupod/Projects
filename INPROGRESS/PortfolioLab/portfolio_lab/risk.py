"""Covariance, portfolio variance, and component risk.

Portfolio variance is wᵀ Σ w. Component risk splits that volatility back
across holdings so the pieces add up to portfolio volatility:

    component_i = w_i * (Σ w)_i / σ_p

Weight times standalone volatility does not add up to portfolio volatility,
so the app never uses it for the risk pie.
"""

from __future__ import annotations

import numpy as np

_VOL_FLOOR = 1e-18


def sample_covariance(returns: np.ndarray) -> np.ndarray:
    """Sample covariance, dividing by n − 1. Rows are dates, columns are assets."""
    values = np.asarray(returns, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2:
        raise ValueError("Need at least two return observations to estimate covariance.")
    if not np.isfinite(values).all():
        raise ValueError("Returns must be finite numbers.")
    centred = values - values.mean(axis=0)
    return (centred.T @ centred) / (values.shape[0] - 1)


def correlation_from_covariance(covariance: np.ndarray) -> np.ndarray:
    """Correlation matrix. Entries are NaN when an asset has zero volatility."""
    covariance = np.asarray(covariance, dtype=float)
    std = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    scale = np.outer(std, std)
    with np.errstate(divide="ignore", invalid="ignore"):
        correlation = np.divide(covariance, scale, out=np.full_like(covariance, np.nan), where=scale > 0)
    np.fill_diagonal(correlation, np.where(std > 0, 1.0, np.nan))
    return correlation


def portfolio_variance(weights: np.ndarray, covariance: np.ndarray) -> float:
    """wᵀ Σ w. Can be zero when the mix is entirely cash."""
    weights = np.asarray(weights, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    variance = float(weights @ covariance @ weights)
    # Tiny negative values are floating-point noise on a singular matrix.
    if variance < 0 and variance > -1e-12:
        return 0.0
    return variance


def portfolio_volatility(weights: np.ndarray, covariance: np.ndarray) -> float:
    variance = portfolio_variance(weights, covariance)
    if variance < 0:
        raise ValueError("Covariance produced a negative portfolio variance.")
    return float(np.sqrt(variance))


def sigma_times_weights(weights: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """The column Σ w, shown as its own step before the dot product."""
    weights = np.asarray(weights, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    return covariance @ weights


def component_risk(weights: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """Volatility contributed by each holding. The pieces sum to portfolio volatility.

    A negative piece is a hedge: that holding reduces portfolio volatility.
    """
    weights = np.asarray(weights, dtype=float)
    volatility = portfolio_volatility(weights, covariance)
    if volatility < _VOL_FLOOR:
        return np.zeros(weights.shape[0], dtype=float)
    marginal = sigma_times_weights(weights, covariance)
    return weights * marginal / volatility
