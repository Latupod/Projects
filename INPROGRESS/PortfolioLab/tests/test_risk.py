import numpy as np
import pytest

from portfolio_lab.hand_example import HAND_RETURNS, HAND_WEIGHTS, HAND_PRICES
from portfolio_lab.returns import annualize_covariance, annualize_mean, simple_returns_matrix
from portfolio_lab.risk import (
    component_risk,
    correlation_from_covariance,
    portfolio_variance,
    portfolio_volatility,
    sample_covariance,
)


def _annual_covariance():
    return annualize_covariance(sample_covariance(HAND_RETURNS))


def test_prices_rebuild_the_hand_returns():
    assert simple_returns_matrix(HAND_PRICES) == pytest.approx(HAND_RETURNS, abs=1e-12)


def test_hand_worked_variance_and_components():
    covariance = _annual_covariance()
    means = annualize_mean(HAND_RETURNS.mean(axis=0))
    assert means == pytest.approx([2.52, 1.26, 1.26], abs=1e-8)
    assert covariance[0, 0] == pytest.approx(0.0504, abs=1e-8)
    assert covariance[0, 1] == pytest.approx(-0.0168, abs=1e-8)
    assert covariance[2, 2] == pytest.approx(0.042, abs=1e-8)
    variance = portfolio_variance(HAND_WEIGHTS, covariance)
    volatility = portfolio_volatility(HAND_WEIGHTS, covariance)
    components = component_risk(HAND_WEIGHTS, covariance)
    assert variance == pytest.approx(0.006972, abs=1e-8)
    assert volatility == pytest.approx(0.08349850298059242, abs=1e-8)
    assert components == pytest.approx(
        [0.09054054540064237, 0.027162163620192713, -0.03420420604024267],
        abs=1e-8,
    )
    assert components.sum() == pytest.approx(volatility, abs=1e-12)


def test_zero_volatility_correlation_is_undefined():
    correlation = correlation_from_covariance(np.array([[0.04, 0.0], [0.0, 0.0]]))
    assert correlation[0, 0] == pytest.approx(1.0)
    assert np.isnan(correlation[0, 1])
