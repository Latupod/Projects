"""Three-asset series used to check the risk formulas by hand.

The daily moves are large on purpose. Annualising four noisy days (mean × 252)
produces enormous expected returns. That is the formula, not a market forecast,
and the README walks through the arithmetic.
"""

from __future__ import annotations

import numpy as np

HAND_NAMES = ["A", "B", "C"]

# Rows are days, columns are A, B, C. Simple returns, not log returns.
HAND_RETURNS = np.array(
    [
        [0.02, 0.01, -0.01],
        [0.01, -0.02, 0.02],
        [-0.01, 0.02, 0.01],
        [0.02, 0.01, 0.00],
    ],
    dtype=float,
)

HAND_WEIGHTS = np.array([0.50, 0.30, 0.20], dtype=float)

# Prices that produce HAND_RETURNS, starting at 100.
HAND_PRICES = np.array(
    [
        [100.0, 102.0, 103.02, 101.9898, 104.029596],
        [100.0, 101.0, 98.98, 100.9596, 101.969196],
        [100.0, 99.0, 100.98, 101.9898, 101.9898],
    ],
    dtype=float,
).T
