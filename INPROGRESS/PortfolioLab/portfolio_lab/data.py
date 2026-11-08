"""Load the sample universe, the price cache, and one portfolio's aligned history."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "data" / "fixtures"
CACHE_DIR = ROOT / "data" / "cache"
UNIVERSE_PATH = FIXTURE_DIR / "universe.json"

WINDOWS = {"1y": 1, "3y": 3, "5y": 5, "all": None}
CASH_TICKER = "CASH"
CASH_NAME = "Cash"


class UnknownTickerError(LookupError):
    """The ticker is not in the sample files or the local cache."""


def load_universe() -> dict:
    with UNIVERSE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def market_info(market: str) -> dict:
    universe = load_universe()
    if market not in universe:
        raise ValueError("Choose the US market or the UK market.")
    return universe[market]


def _read_csv(path: Path) -> pd.Series:
    frame = pd.read_csv(path, parse_dates=["date"])
    if "close" not in frame.columns or frame.empty:
        raise ValueError(f"{path.name} has no close prices.")
    series = frame.sort_values("date").set_index("date")["close"].astype(float)
    series.index = pd.to_datetime(series.index)
    series = series[~series.index.duplicated(keep="last")]
    if series.le(0).any() or not np.isfinite(series.to_numpy()).all():
        raise ValueError(f"{path.name} contains a price that is not a positive number.")
    return series


def _read_meta(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fixture_assets(market: str) -> dict[str, dict]:
    info = market_info(market)
    assets = {asset["ticker"]: dict(asset) for asset in info["assets"]}
    benchmark = dict(info["benchmark"])
    benchmark["kind"] = "benchmark"
    assets[benchmark["ticker"]] = benchmark
    return assets


def _cache_dir(market: str) -> Path:
    return CACHE_DIR / market


def list_assets(market: str) -> list[dict]:
    """Selectable holdings: the sample list, plus live tickers cached for this market."""
    info = market_info(market)
    assets = []
    for asset in info["assets"]:
        merged = dict(asset)
        cached = _read_meta(_cache_dir(market) / f"{asset['ticker']}.json")
        if cached and cached.get("dividend_yield") is not None:
            merged["dividend_yield"] = cached["dividend_yield"]
        merged["source"] = "cache" if (_cache_dir(market) / f"{asset['ticker']}.csv").exists() else "sample"
        assets.append(merged)
    known = {asset["ticker"] for asset in assets}
    cache_dir = _cache_dir(market)
    if cache_dir.exists():
        for meta_path in sorted(cache_dir.glob("*.json")):
            ticker = meta_path.stem
            if ticker in known or ticker == info["benchmark"]["ticker"]:
                continue
            meta = _read_meta(meta_path) or {"ticker": ticker, "name": ticker}
            meta["source"] = "cache"
            meta.setdefault("kind", "live")
            assets.append(meta)
    return assets


def resolve_prices(market: str, ticker: str) -> tuple[pd.Series, dict]:
    """Cache wins over the sample file. Metadata falls back to the sample universe."""
    fixtures = _fixture_assets(market)
    cache_csv = _cache_dir(market) / f"{ticker}.csv"
    fixture_csv = FIXTURE_DIR / market / f"{ticker}.csv"
    meta = dict(fixtures.get(ticker, {}))
    cached_meta = _read_meta(_cache_dir(market) / f"{ticker}.json")
    if cached_meta:
        meta.update({key: value for key, value in cached_meta.items() if value is not None})
    if cache_csv.exists():
        prices = _read_csv(cache_csv)
    elif fixture_csv.exists():
        prices = _read_csv(fixture_csv)
    else:
        raise UnknownTickerError(f"{ticker} is not in the {market} sample data or the local cache.")
    meta.setdefault("ticker", ticker)
    meta.setdefault("name", ticker)
    meta.setdefault("kind", "live")
    return prices, meta


def slice_window(prices: pd.DataFrame, window: str) -> tuple[pd.DataFrame, str | None]:
    """Keep the last 1, 3, or 5 years, or the whole file. Note when the file is shorter."""
    if window not in WINDOWS:
        raise ValueError("Window must be 1y, 3y, 5y, or all.")
    if prices.empty:
        raise ValueError("There are no prices in this window.")
    years = WINDOWS[window]
    if years is None:
        return prices, None
    end = prices.index.max()
    start = end - pd.DateOffset(years=years)
    sliced = prices.loc[prices.index >= start]
    if sliced.empty:
        raise ValueError("There are no prices in this window.")
    if prices.index.min() > start + pd.Timedelta(days=31):
        note = (
            f"The file does not go back a full {years} years, so this window uses everything available "
            f"({len(sliced)} price days)."
        )
        return sliced, note
    return sliced, None


def aligned_prices(market: str, tickers: list[str], window: str) -> tuple[pd.DataFrame, list[dict], str | None]:
    """Inner-join prices so every column has a price on the same dates."""
    if not tickers:
        raise ValueError("Select at least one stock or ETF.")
    frames = []
    metas = []
    for ticker in tickers:
        series, meta = resolve_prices(market, ticker)
        frames.append(series.rename(ticker))
        metas.append(meta)
    combined = pd.concat(frames, axis=1, join="inner").sort_index().dropna()
    combined, note = slice_window(combined, window)
    if len(combined) < 3:
        raise ValueError(
            "Not enough overlapping prices in this window. Choose a longer window or different holdings."
        )
    return combined, metas, note


def normalize_quote(prices: pd.Series, currency: str | None) -> tuple[pd.Series, str, str | None]:
    """Convert London pence quotes (GBp / GBX) into pounds when the level looks like pence.

    Some downloads label a series GBp even after the prices have already been
    converted to pounds. Those series are left as they are, and the note says so.
    """
    code = (currency or "").strip()
    if code in {"GBp", "GBX"}:
        median = float(prices.median())
        if median >= 100:
            return prices / 100.0, "GBP", "Interpreted these prices as pence and converted them to pounds."
        return (
            prices,
            "GBP",
            "The source labelled the currency as pence, but the prices already look like pounds, so they were left unchanged.",
        )
    if not code:
        return prices, "unknown", None
    return prices, code, None
