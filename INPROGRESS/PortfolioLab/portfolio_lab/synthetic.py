"""Build a deterministic sample universe. These files are synthetic, not downloaded prices."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from portfolio_lab.data import FIXTURE_DIR

START = "2021-11-01"
END = "2026-10-30"


def _nearest_correlation(matrix: np.ndarray) -> np.ndarray:
    symmetric = (matrix + matrix.T) / 2.0
    values, vectors = np.linalg.eigh(symmetric)
    values = np.clip(values, 1e-6, None)
    repaired = vectors @ np.diag(values) @ vectors.T
    scale = np.sqrt(np.diag(repaired))
    repaired = repaired / np.outer(scale, scale)
    np.fill_diagonal(repaired, 1.0)
    return repaired


def _simulate(spec: list[dict], correlation: np.ndarray, seed: int) -> dict[str, pd.Series]:
    dates = pd.bdate_range(START, END)
    generator = np.random.default_rng(seed)
    means = np.array([row["mean"] for row in spec], dtype=float) / 252.0
    vols = np.array([row["vol"] for row in spec], dtype=float) / np.sqrt(252.0)
    covariance = _nearest_correlation(correlation) * np.outer(vols, vols)
    factor = np.linalg.cholesky(covariance + np.eye(len(spec)) * 1e-12)
    shocks = generator.standard_normal((len(dates) - 1, len(spec)))
    returns = means + shocks @ factor.T
    series = {}
    for index, row in enumerate(spec):
        prices = [float(row["start"])]
        for daily in returns[:, index]:
            prices.append(prices[-1] * (1.0 + float(daily)))
        series[row["ticker"]] = pd.Series(prices, index=dates, name=row["ticker"])
    return series


def _write_series(market: str, series: dict[str, pd.Series]) -> None:
    folder = FIXTURE_DIR / market
    folder.mkdir(parents=True, exist_ok=True)
    for ticker, prices in series.items():
        frame = pd.DataFrame({"date": prices.index.strftime("%Y-%m-%d"), "close": np.round(prices.to_numpy(), 6)})
        frame.to_csv(folder / f"{ticker}.csv", index=False, lineterminator="\n")


def build_fixtures() -> None:
    """Regenerate data/fixtures for the US and UK sample markets."""
    us = [
        {"ticker": "AAPL", "name": "Apple", "kind": "stock", "mean": 0.12, "vol": 0.22, "start": 150.0, "dividend_yield": 0.005},
        {"ticker": "MSFT", "name": "Microsoft", "kind": "stock", "mean": 0.11, "vol": 0.20, "start": 300.0, "dividend_yield": 0.008},
        {"ticker": "JNJ", "name": "Johnson & Johnson", "kind": "stock", "mean": 0.07, "vol": 0.14, "start": 160.0, "dividend_yield": 0.032},
        {"ticker": "XOM", "name": "Exxon Mobil", "kind": "stock", "mean": 0.09, "vol": 0.24, "start": 100.0, "dividend_yield": 0.034},
        {"ticker": "SPY", "name": "SPDR S&P 500 ETF", "kind": "etf", "mean": 0.10, "vol": 0.16, "start": 400.0, "dividend_yield": 0.013},
        {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "kind": "etf", "mean": 0.04, "vol": 0.05, "start": 75.0, "dividend_yield": 0.038},
        {"ticker": "SPX", "name": "S&P 500", "kind": "benchmark", "mean": 0.10, "vol": 0.15, "start": 4500.0, "dividend_yield": None},
    ]
    us_corr = np.array(
        [
            [1.00, 0.70, 0.30, 0.25, 0.80, 0.05, 0.75],
            [0.70, 1.00, 0.35, 0.20, 0.82, 0.05, 0.78],
            [0.30, 0.35, 1.00, 0.20, 0.50, 0.10, 0.45],
            [0.25, 0.20, 0.20, 1.00, 0.40, -0.05, 0.35],
            [0.80, 0.82, 0.50, 0.40, 1.00, 0.08, 0.95],
            [0.05, 0.05, 0.10, -0.05, 0.08, 1.00, 0.05],
            [0.75, 0.78, 0.45, 0.35, 0.95, 0.05, 1.00],
        ]
    )
    uk = [
        {"ticker": "SHEL.L", "name": "Shell", "kind": "stock", "mean": 0.08, "vol": 0.22, "start": 27.0, "dividend_yield": 0.038},
        {"ticker": "AZN.L", "name": "AstraZeneca", "kind": "stock", "mean": 0.09, "vol": 0.20, "start": 110.0, "dividend_yield": None},
        {"ticker": "HSBA.L", "name": "HSBC", "kind": "stock", "mean": 0.08, "vol": 0.24, "start": 6.5, "dividend_yield": 0.055},
        {"ticker": "ULVR.L", "name": "Unilever", "kind": "stock", "mean": 0.06, "vol": 0.16, "start": 40.0, "dividend_yield": 0.032},
        {"ticker": "ISF.L", "name": "iShares Core FTSE 100 ETF", "kind": "etf", "mean": 0.07, "vol": 0.14, "start": 8.0, "dividend_yield": 0.035},
        {"ticker": "IGLT.L", "name": "iShares Core UK Gilts ETF", "kind": "etf", "mean": 0.03, "vol": 0.08, "start": 12.0, "dividend_yield": 0.030},
        {"ticker": "FTSE", "name": "FTSE 100", "kind": "benchmark", "mean": 0.07, "vol": 0.13, "start": 7500.0, "dividend_yield": None},
    ]
    uk_corr = np.array(
        [
            [1.00, 0.25, 0.40, 0.30, 0.70, 0.05, 0.72],
            [0.25, 1.00, 0.20, 0.30, 0.45, 0.08, 0.40],
            [0.40, 0.20, 1.00, 0.25, 0.65, -0.05, 0.68],
            [0.30, 0.30, 0.25, 1.00, 0.50, 0.10, 0.48],
            [0.70, 0.45, 0.65, 0.50, 1.00, 0.08, 0.96],
            [0.05, 0.08, -0.05, 0.10, 0.08, 1.00, 0.06],
            [0.72, 0.40, 0.68, 0.48, 0.96, 0.06, 1.00],
        ]
    )
    _write_series("US", _simulate(us, us_corr, seed=7))
    _write_series("UK", _simulate(uk, uk_corr, seed=11))
    universe = {
        "US": {
            "currency": "USD",
            "currency_label": "US dollars",
            "benchmark": {"ticker": "SPX", "name": "S&P 500"},
            "assets": [_public(row) for row in us if row["kind"] != "benchmark"],
        },
        "UK": {
            "currency": "GBP",
            "currency_label": "pounds",
            "benchmark": {"ticker": "FTSE", "name": "FTSE 100"},
            "assets": [_public(row) for row in uk if row["kind"] != "benchmark"],
        },
    }
    (FIXTURE_DIR / "universe.json").write_text(json.dumps(universe, indent=2), encoding="utf-8")
    _write_hand_example()


def _public(row: dict) -> dict:
    return {
        "ticker": row["ticker"],
        "name": row["name"],
        "kind": row["kind"],
        "dividend_yield": row["dividend_yield"],
    }


def _write_hand_example() -> None:
    from portfolio_lab.hand_example import HAND_NAMES, HAND_PRICES

    folder = FIXTURE_DIR / "hand"
    folder.mkdir(parents=True, exist_ok=True)
    dates = pd.bdate_range("2024-01-02", periods=HAND_PRICES.shape[0])
    for index, name in enumerate(HAND_NAMES):
        frame = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "close": HAND_PRICES[:, index]})
        frame.to_csv(folder / f"{name}.csv", index=False, lineterminator="\n")


def main() -> None:
    build_fixtures()
    print(f"Wrote sample fixtures to {FIXTURE_DIR}")


if __name__ == "__main__":
    main()
