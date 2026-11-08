import numpy as np
import pandas as pd

from portfolio_lab.stats import best_worst_month, max_drawdown, sharpe_ratio


def test_max_drawdown_is_the_largest_peak_to_trough_loss():
    # Wealth goes 1 -> 1.1 -> 0.55 -> 0.66, so the worst fall is 50%.
    assert max_drawdown(np.array([0.10, -0.50, 0.20])) == pytest_approx(0.5)


def test_sharpe_is_undefined_when_volatility_is_zero():
    assert sharpe_ratio(0.04, 0.0, 0.02) is None
    assert sharpe_ratio(0.10, 0.20, 0.02) == pytest_approx(0.4)


def test_best_and_worst_month():
    index = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-02-01", "2024-02-02"])
    series = pd.Series([0.10, 0.0, -0.20, 0.0], index=index)
    months = best_worst_month(series)
    assert months["best"]["label"] == "2024-01"
    assert months["best"]["return"] == pytest_approx(0.10)
    assert months["worst"]["label"] == "2024-02"
    assert months["worst"]["return"] == pytest_approx(-0.20)


def pytest_approx(value):
    import pytest

    return pytest.approx(value)
