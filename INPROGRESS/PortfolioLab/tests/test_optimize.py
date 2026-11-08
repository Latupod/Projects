import numpy as np
import pytest

from portfolio_lab.optimize import (
    GROWTH_CASH_CAP,
    InfeasibleError,
    efficient_frontier,
    equal_weight,
    maximum_sharpe,
    minimum_variance,
    standard_bounds,
    user_weights,
)
from portfolio_lab.risk import portfolio_volatility


MEANS = np.array([0.08, 0.12, 0.05])
COVARIANCE = np.array(
    [
        [0.04, 0.01, 0.00],
        [0.01, 0.09, 0.02],
        [0.00, 0.02, 0.01],
    ]
)


def test_caps_that_cannot_reach_100_percent_are_rejected():
    with pytest.raises(InfeasibleError, match="can only cover 60%"):
        standard_bounds(3, 0.20)


def test_user_weights_scale_to_100_and_reject_a_cap_breach():
    weights, scaled = user_weights(np.array([2.0, 2.0, 2.0]), [(0.0, 1.0)] * 3)
    assert scaled
    assert weights == pytest.approx([1 / 3, 1 / 3, 1 / 3])
    with pytest.raises(InfeasibleError, match="above the cap"):
        user_weights(np.array([0.9, 0.3]), [(0.0, 0.6), (0.0, 0.6)])
    with pytest.raises(InfeasibleError, match="negative"):
        user_weights(np.array([1.2, -0.2]), [(0.0, 1.0), (0.0, 1.0)])


def test_locked_cash_can_push_equal_weight_through_the_cap():
    bounds = [(0.0, 0.8), (0.0, 0.4), (0.0, 0.4)]
    with pytest.raises(InfeasibleError, match="above the cap"):
        equal_weight(bounds, cash_index=0, locked_cash_weight=0.10)


def test_minimum_variance_is_the_lowest_of_the_three():
    bounds = [(0.0, 0.6)] * 3
    equal = equal_weight(bounds)
    cautious = minimum_variance(COVARIANCE, bounds)
    balanced = maximum_sharpe(MEANS, COVARIANCE, 0.03, bounds)
    for weights in (equal, cautious, balanced):
        assert weights.sum() == pytest.approx(1.0)
        assert np.all(weights >= -1e-8)
        assert np.all(weights <= 0.6 + 1e-8)
    cautious_vol = portfolio_volatility(cautious, COVARIANCE)
    assert cautious_vol <= portfolio_volatility(equal, COVARIANCE) + 1e-6
    assert cautious_vol <= portfolio_volatility(balanced, COVARIANCE) + 1e-6


def test_override_changes_sharpe_weights_not_the_covariance():
    bounds = [(0.0, 1.0), (0.0, 1.0)]
    covariance = np.array([[0.04, 0.01], [0.01, 0.05]])
    original = covariance.copy()
    base = maximum_sharpe(np.array([0.06, 0.07]), covariance, 0.02, bounds)
    shifted = maximum_sharpe(np.array([0.30, 0.07]), covariance, 0.02, bounds)
    assert covariance == pytest.approx(original)
    assert base != pytest.approx(shifted, abs=1e-3)
    assert shifted[0] > base[0]


def test_cash_takes_the_minimum_variance_portfolio_when_it_is_allowed():
    covariance = np.array(
        [
            [0.04, 0.01, 0.0],
            [0.01, 0.09, 0.0],
            [0.0, 0.0, 0.0],
        ]
    )
    uncapped = minimum_variance(covariance, [(0.0, 1.0)] * 3)
    assert uncapped[2] == pytest.approx(1.0, abs=1e-4)
    capped = minimum_variance(covariance, [(0.0, 0.4)] * 3)
    assert capped[2] == pytest.approx(0.4, abs=1e-3)
    assert capped.sum() == pytest.approx(1.0)


def test_growth_caps_cash_at_10_percent():
    means = np.array([0.08, 0.09, 0.50])
    covariance = np.array(
        [
            [0.04, 0.01, 0.0],
            [0.01, 0.05, 0.0],
            [0.0, 0.0, 0.0],
        ]
    )
    balanced_bounds = standard_bounds(3, 1.0, cash_index=2, growth=False)
    growth_bounds = standard_bounds(3, 1.0, cash_index=2, growth=True)
    balanced = maximum_sharpe(means, covariance, 0.02, balanced_bounds)
    growth = maximum_sharpe(means, covariance, 0.02, growth_bounds)
    assert balanced[2] > 0.5
    assert growth[2] <= GROWTH_CASH_CAP + 1e-6
    assert growth.sum() == pytest.approx(1.0)


def test_frontier_bottom_is_the_minimum_variance_portfolio():
    bounds = [(0.0, 0.7)] * 3
    cautious = minimum_variance(COVARIANCE, bounds)
    points = efficient_frontier(MEANS, COVARIANCE, bounds, n_points=11)
    assert len(points) >= 2
    lowest = min(point["volatility"] for point in points)
    assert lowest <= portfolio_volatility(cautious, COVARIANCE) + 1e-3
