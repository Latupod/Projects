import numpy as np
import pytest

from portfolio_lab.analysis import _sample_warning, analyse


def _spec(**overrides):
    spec = {
        "market": "US",
        "tickers": ["AAPL", "MSFT", "BND"],
        "weights": {"AAPL": 0.3, "MSFT": 0.3, "BND": 0.4},
        "strategy": "max_sharpe",
        "window": "1y",
        "risk_free_rate": 0.04,
        "max_weight": 1.0,
        "include_cash": False,
        "cash_yield": 0.04,
        "cash_weight": None,
        "expected_return_overrides": {},
    }
    spec.update(overrides)
    return spec


def _weights(result, key):
    row = next(item for item in result["comparison"] if item["key"] == key)
    assert row["ok"], row.get("error")
    return [item["weight"] for item in row["weights"]]


def test_sample_warning_fires_for_a_short_noisy_window():
    assert _sample_warning(30, 5)
    assert _sample_warning(400, 3) is None


def test_override_does_not_change_covariance_or_minimum_variance():
    base = analyse(_spec())
    shifted = analyse(_spec(expected_return_overrides={"AAPL": 0.35}))
    assert np.allclose(base["math"]["covariance"], shifted["math"]["covariance"])
    assert _weights(base, "min_variance") == pytest.approx(_weights(shifted, "min_variance"), abs=1e-6)
    assert _weights(base, "max_sharpe") != pytest.approx(_weights(shifted, "max_sharpe"), abs=1e-3)


def test_lesson_mix_reports_risk_shares_and_a_missing_dividend():
    us = analyse(
        _spec(
            tickers=["AAPL", "MSFT", "JNJ", "XOM", "SPY", "BND"],
            strategy="min_variance",
            max_weight=0.4,
            include_cash=True,
            window="3y",
        )
    )
    assert us["ok"]
    assert sum(us["math"]["weights"]) == pytest.approx(1.0)
    assert sum(us["math"]["component_risk"]) == pytest.approx(us["math"]["volatility"], abs=1e-8)
    assert us["charts"]["frontier"]
    assert us["charts"]["growth"]["benchmark"]
    assert us["portfolio"]["best_month"]["label"]
    assert us["portfolio"]["worst_month"]["return"] <= us["portfolio"]["best_month"]["return"]

    uk = analyse(
        _spec(
            market="UK",
            tickers=["AZN.L", "SHEL.L"],
            weights={"AZN.L": 0.5, "SHEL.L": 0.5},
            strategy="equal",
            max_weight=0.7,
        )
    )
    by_ticker = {asset["ticker"]: asset for asset in uk["assets"]}
    assert by_ticker["AZN.L"]["dividend_yield"] is None
    assert by_ticker["SHEL.L"]["dividend_yield"] == pytest.approx(0.038)
    assert uk["assets"][0]["max_drawdown"] >= 0
