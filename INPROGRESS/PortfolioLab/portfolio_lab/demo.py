"""Print the hand-worked weight vector, covariance, and portfolio variance."""

from __future__ import annotations

import numpy as np

from portfolio_lab.hand_example import HAND_NAMES, HAND_RETURNS, HAND_WEIGHTS
from portfolio_lab.returns import annualize_covariance, annualize_mean
from portfolio_lab.risk import component_risk, portfolio_variance, portfolio_volatility, sample_covariance, sigma_times_weights


def _column(names: list[str], values: np.ndarray, places: int = 6) -> str:
    lines = []
    for name, value in zip(names, values):
        lines.append(f"  {name:<4} {value:+.{places}f}")
    return "\n".join(lines)


def _matrix(names: list[str], matrix: np.ndarray) -> str:
    header = "      " + " ".join(f"{name:>12}" for name in names)
    lines = [header]
    for name, row in zip(names, matrix):
        cells = " ".join(f"{value:+12.6f}" for value in row)
        lines.append(f"  {name:<4} {cells}")
    return "\n".join(lines)


def main() -> None:
    covariance = annualize_covariance(sample_covariance(HAND_RETURNS))
    means = annualize_mean(HAND_RETURNS.mean(axis=0))
    sigma_w = sigma_times_weights(HAND_WEIGHTS, covariance)
    variance = portfolio_variance(HAND_WEIGHTS, covariance)
    volatility = portfolio_volatility(HAND_WEIGHTS, covariance)
    components = component_risk(HAND_WEIGHTS, covariance)
    print("Hand-worked 3-asset example")
    print("Simple daily returns, annualised by multiplying by 252.")
    print("Sample covariance divides by n - 1.")
    print()
    print("Annualised mean return:")
    print(_column(HAND_NAMES, means))
    print()
    print("Weights w:")
    print(_column(HAND_NAMES, HAND_WEIGHTS))
    print()
    print("Annualised covariance Sigma:")
    print(_matrix(HAND_NAMES, covariance))
    print()
    print("Sigma w:")
    print(_column(HAND_NAMES, sigma_w))
    print()
    print(f"variance = w' (Sigma w) = {variance:.6f}")
    print(f"volatility = sqrt(variance) = {volatility:.6f}")
    print()
    print("Component risk (these sum to volatility):")
    print(_column(HAND_NAMES, components))
    print(f"  sum  {components.sum():+.6f}")


if __name__ == "__main__":
    main()
