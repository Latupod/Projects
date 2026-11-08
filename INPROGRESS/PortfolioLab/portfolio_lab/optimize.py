"""Long-only portfolios: equal weight, minimum variance, maximum Sharpe, and the frontier.

Every strategy forces weights to add up to 100% and keeps each holding inside
its cap. Short sales are not allowed. Growth is maximum Sharpe with cash
capped at 10% as well.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

GROWTH_CASH_CAP = 0.10
_TOL = 1e-9


class InfeasibleError(ValueError):
    """The caps, locks, or weight entries cannot form a 100% long-only mix."""


def assert_feasible(bounds: list[tuple[float, float]]) -> None:
    """Reject a cap set that cannot add up to 100%."""
    if not bounds:
        raise InfeasibleError("Select at least one holding.")
    lows = np.array([low for low, _ in bounds], dtype=float)
    highs = np.array([high for _, high in bounds], dtype=float)
    if np.any(highs < lows - _TOL):
        raise InfeasibleError("A holding has a cap below its minimum weight.")
    if lows.sum() > 1 + 1e-8:
        raise InfeasibleError("The minimum weights already add up to more than 100%.")
    if highs.sum() < 1 - 1e-8:
        cover = float(highs.sum())
        if np.allclose(highs, highs[0]):
            raise InfeasibleError(
                f"These caps cannot add up to 100%. {len(bounds)} holdings with a cap of "
                f"{highs[0]:.0%} can only cover {cover:.0%}. Raise the cap or add another holding."
            )
        raise InfeasibleError(
            f"These caps cannot add up to 100%. The most you can allocate is {cover:.0%}. "
            "Raise a cap or add another holding."
        )


def standard_bounds(n_assets: int, max_weight: float, cash_index: int | None = None, growth: bool = False) -> list[tuple[float, float]]:
    """Long-only bounds. Growth also caps cash at 10%."""
    if n_assets < 1:
        raise InfeasibleError("Select at least one holding.")
    cap = float(max_weight)
    if not np.isfinite(cap) or cap <= 0 or cap > 1:
        raise InfeasibleError("The per-holding cap must be above 0% and at most 100%.")
    bounds = [(0.0, cap) for _ in range(n_assets)]
    if growth and cash_index is not None:
        bounds[cash_index] = (0.0, min(cap, GROWTH_CASH_CAP))
    assert_feasible(bounds)
    return bounds


def clean_weights(weights: np.ndarray, bounds: list[tuple[float, float]]) -> np.ndarray:
    """Clip tiny solver noise and nudge the weights back onto 100%."""
    assert_feasible(bounds)
    lows = np.array([low for low, _ in bounds], dtype=float)
    highs = np.array([high for _, high in bounds], dtype=float)
    cleaned = np.minimum(np.maximum(np.asarray(weights, dtype=float), lows), highs)
    for _ in range(30):
        gap = 1.0 - float(cleaned.sum())
        if abs(gap) < 1e-10:
            break
        if gap > 0:
            room = highs - cleaned
        else:
            room = cleaned - lows
        free = room > 1e-12
        if not np.any(free):
            raise InfeasibleError(
                "These caps cannot add up to 100%. Raise the cap or add another holding."
            )
        cleaned[free] += gap * room[free] / room[free].sum()
        cleaned = np.minimum(np.maximum(cleaned, lows), highs)
    if abs(float(cleaned.sum()) - 1.0) > 1e-7:
        raise InfeasibleError(
            "These caps cannot add up to 100%. Raise the cap or add another holding."
        )
    cleaned[np.abs(cleaned) < 1e-8] = 0.0
    if np.any(cleaned < -1e-8) or np.any(cleaned > highs + 1e-8):
        raise InfeasibleError("A weight landed outside its cap.")
    return cleaned


def user_weights(raw_weights: np.ndarray, bounds: list[tuple[float, float]]) -> tuple[np.ndarray, bool]:
    """Score the weights you typed. Scale them only when they do not already sum to 100%."""
    weights = np.asarray(raw_weights, dtype=float)
    if weights.shape != (len(bounds),):
        raise InfeasibleError("Enter one weight for each holding.")
    if not np.isfinite(weights).all():
        raise InfeasibleError("Weights must be numbers.")
    if np.any(weights < -1e-10):
        raise InfeasibleError("Weights cannot be negative in this tool.")
    if float(weights.sum()) <= 1e-12:
        raise InfeasibleError("Enter weights that add up to more than zero.")
    scaled = abs(float(weights.sum()) - 1.0) > 1e-6
    if scaled:
        weights = weights / weights.sum()
    highs = np.array([high for _, high in bounds], dtype=float)
    if np.any(weights > highs + 1e-8):
        raise InfeasibleError(
            "After making the weights add up to 100%, at least one holding is above the cap. "
            "Lower that weight or raise the cap."
        )
    return clean_weights(weights, bounds), scaled


def equal_weight(
    bounds: list[tuple[float, float]],
    cash_index: int | None = None,
    locked_cash_weight: float | None = None,
) -> np.ndarray:
    """Split the risky holdings equally. Locked cash stays put; otherwise cash joins the split."""
    assert_feasible(bounds)
    n_assets = len(bounds)
    weights = np.zeros(n_assets, dtype=float)
    if cash_index is not None and locked_cash_weight is not None:
        locked = float(locked_cash_weight)
        low, high = bounds[cash_index]
        if not np.isfinite(locked) or locked < low - 1e-8 or locked > high + 1e-8:
            raise InfeasibleError("The locked cash weight is outside its allowed range.")
        weights[cash_index] = locked
        others = [index for index in range(n_assets) if index != cash_index]
        if not others:
            if abs(locked - 1.0) > 1e-8:
                raise InfeasibleError("Cash is the only holding, so its weight has to be 100%.")
            return clean_weights(weights, bounds)
        share = (1.0 - locked) / len(others)
        for index in others:
            high = bounds[index][1]
            if share > high + 1e-8:
                raise InfeasibleError(
                    f"Equal weight would put {share:.0%} in each other holding, which is above the cap. "
                    "Raise the cap, unlock cash, or add another holding."
                )
            weights[index] = share
        return clean_weights(weights, bounds)

    share = 1.0 / n_assets
    for index, (_, high) in enumerate(bounds):
        if share > high + 1e-8:
            raise InfeasibleError(
                f"Equal weight would put {share:.0%} in each holding, which is above the cap. "
                "Raise the cap or add another holding."
            )
        weights[index] = share
    return clean_weights(weights, bounds)


def _greedy(scores: np.ndarray, bounds: list[tuple[float, float]], *, prefer_high: bool) -> np.ndarray:
    """Fill holdings in score order, up to each cap, until the weights sum to 100%."""
    assert_feasible(bounds)
    order = np.argsort(np.asarray(scores, dtype=float))
    if prefer_high:
        order = order[::-1]
    weights = np.array([low for low, _ in bounds], dtype=float)
    remaining = 1.0 - float(weights.sum())
    for index in order:
        if remaining <= 1e-12:
            break
        room = bounds[index][1] - weights[index]
        take = min(max(room, 0.0), remaining)
        weights[index] += take
        remaining -= take
    return clean_weights(weights, bounds)


def _starts(
    bounds: list[tuple[float, float]],
    scores: np.ndarray | None = None,
    n_random: int = 6,
) -> list[np.ndarray]:
    starts = []
    if scores is not None:
        starts.append(_greedy(scores, bounds, prefer_high=False))
        starts.append(_greedy(scores, bounds, prefer_high=True))
    else:
        starts.append(_greedy(np.zeros(len(bounds)), bounds, prefer_high=False))
    generator = np.random.default_rng(1)
    for _ in range(n_random):
        draw = generator.random(len(bounds))
        starts.append(clean_weights(draw, bounds))
    return starts


def _solve(
    objective,
    bounds: list[tuple[float, float]],
    starts: list[np.ndarray],
    extra_constraints: list | None = None,
) -> np.ndarray:
    constraints = [{"type": "eq", "fun": lambda weights: np.sum(weights) - 1.0}]
    if extra_constraints:
        constraints.extend(extra_constraints)
    best_weights = None
    best_value = np.inf
    for start in starts:
        result = minimize(
            objective,
            start,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"maxiter": 400, "ftol": 1e-12, "disp": False},
        )
        if not result.success and not np.isfinite(result.fun):
            continue
        candidate = np.asarray(result.x, dtype=float)
        try:
            candidate = clean_weights(candidate, bounds)
        except InfeasibleError:
            continue
        value = float(objective(candidate))
        if np.isfinite(value) and value < best_value:
            best_value = value
            best_weights = candidate
    if best_weights is None:
        raise InfeasibleError(
            "The optimiser could not find weights under these caps. Try a higher cap or fewer holdings."
        )
    return best_weights


def minimum_variance(
    covariance: np.ndarray,
    bounds: list[tuple[float, float]],
    target_return: tuple[np.ndarray, float] | None = None,
    n_random_starts: int = 6,
) -> np.ndarray:
    """Lowest wᵀ Σ w. Pass a target return to trace one point on the frontier."""
    covariance = np.asarray(covariance, dtype=float)
    variances = np.clip(np.diag(covariance), 0.0, None)

    def objective(weights: np.ndarray) -> float:
        return float(weights @ covariance @ weights)

    constraints = None
    if target_return is not None:
        means, target = target_return
        means = np.asarray(means, dtype=float)
        target = float(target)

        def _hit_target(weights: np.ndarray, means=means, target=target) -> float:
            return float(weights @ means - target)

        constraints = [{"type": "eq", "fun": _hit_target}]
    return _solve(objective, bounds, _starts(bounds, variances, n_random_starts), constraints)


def maximum_sharpe(
    means: np.ndarray,
    covariance: np.ndarray,
    risk_free_rate: float,
    bounds: list[tuple[float, float]],
) -> np.ndarray:
    """Maximise (w · μ − rf) / σ. Because the weights sum to 1 this is w · (μ − rf) / σ."""
    means = np.asarray(means, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    excess = means - float(risk_free_rate)

    def objective(weights: np.ndarray) -> float:
        variance = float(weights @ covariance @ weights)
        volatility = np.sqrt(variance) if variance > 0 else 0.0
        portfolio_excess = float(weights @ excess)
        if volatility < 1e-10:
            # A zero-volatility mix has no Sharpe ratio. Prefer it when it still
            # beats the risk-free rate, so cash can win when its yield is higher.
            if portfolio_excess >= 0:
                return -1e6 - portfolio_excess
            return 1e6 - portfolio_excess
        return -(portfolio_excess / volatility)

    return _solve(objective, bounds, _starts(bounds, excess), None)


def efficient_frontier(
    means: np.ndarray,
    covariance: np.ndarray,
    bounds: list[tuple[float, float]],
    n_points: int = 21,
) -> list[dict]:
    """Minimise variance at a grid of target expected returns between the feasible extremes."""
    means = np.asarray(means, dtype=float)
    low = _greedy(means, bounds, prefer_high=False)
    high = _greedy(means, bounds, prefer_high=True)
    low_return = float(low @ means)
    high_return = float(high @ means)
    if high_return - low_return < 1e-10:
        targets = np.array([low_return])
    else:
        targets = np.linspace(low_return, high_return, n_points)
    points = []
    for target in targets:
        try:
            weights = minimum_variance(
                covariance, bounds, target_return=(means, float(target)), n_random_starts=1
            )
        except InfeasibleError:
            continue
        variance = float(weights @ covariance @ weights)
        volatility = float(np.sqrt(variance)) if variance > 0 else 0.0
        points.append(
            {
                "expected_return": float(weights @ means),
                "volatility": volatility,
                "weights": weights,
            }
        )
    return points
