"""Optional Yahoo Finance download into data/cache. The sample files keep working offline."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from portfolio_lab.data import CACHE_DIR, normalize_quote

_SYMBOL = re.compile(r"^[A-Za-z0-9^][A-Za-z0-9.\-]{0,14}$")


def clean_symbol(symbol: str) -> str:
    """Reject anything that could escape the cache directory."""
    text = (symbol or "").strip()
    if not _SYMBOL.fullmatch(text) or text in {".", ".."}:
        raise ValueError("Enter a ticker such as AAPL or SHEL.L. Letters, numbers, a dot, or a caret only.")
    return text


def _dividend_yield(info: dict) -> float | None:
    """Yahoo's dividend field is sometimes a fraction and sometimes a percent."""
    raw = info.get("dividendYield") if isinstance(info, dict) else None
    if raw is None:
        trailing = info.get("trailingAnnualDividendYield") if isinstance(info, dict) else None
        raw = trailing
    if raw is None:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if not pd.notna(value):
        return None
    if value > 0.25:
        value = value / 100.0
    if value < 0 or value > 0.25:
        return None
    return value


def store_history(
    symbol: str,
    market: str,
    closes: pd.Series,
    currency: str | None,
    dividend_yield: float | None,
    name: str | None,
) -> dict:
    """Write the same CSV shape as the sample files, in major currency units."""
    symbol = clean_symbol(symbol)
    if market not in {"US", "UK"}:
        raise ValueError("Choose the US market or the UK market.")
    prices, resolved_currency, note = normalize_quote(closes.astype(float), currency)
    prices = prices.dropna().sort_index()
    prices.index = pd.to_datetime(prices.index)
    if getattr(prices.index, "tz", None) is not None:
        prices.index = prices.index.tz_convert(None)
    if prices.empty:
        raise LookupError(f"No prices returned for {symbol}. Check the ticker symbol.")
    folder = CACHE_DIR / market
    folder.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame({"date": prices.index.strftime("%Y-%m-%d"), "close": prices.to_numpy()})
    frame.to_csv(folder / f"{symbol}.csv", index=False)
    meta = {
        "ticker": symbol,
        "name": name or symbol,
        "kind": "live",
        "currency": resolved_currency,
        "source_currency": currency,
        "dividend_yield": dividend_yield,
        "note": note,
        "source": "yfinance",
    }
    (folder / f"{symbol}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def fetch_to_cache(symbol: str, market: str) -> dict:
    """Download adjusted history. Failures stay as messages; the sample data is untouched."""
    symbol = clean_symbol(symbol)
    if market not in {"US", "UK"}:
        raise ValueError("Choose the US market or the UK market.")
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance is not installed. Run pip install -r requirements.txt.") from exc
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5y", auto_adjust=True)
    except Exception as exc:  # network, rate limit, or an unknown symbol
        raise LookupError(
            f"Could not download {symbol}. Check the symbol, then try again. ({exc.__class__.__name__})"
        ) from exc
    if history is None or history.empty or "Close" not in history.columns:
        raise LookupError(f"No prices returned for {symbol}. Check the ticker symbol.")
    currency = None
    name = symbol
    dividend = None
    try:
        fast = ticker.fast_info
        currency = fast.get("currency") if hasattr(fast, "get") else getattr(fast, "currency", None)
    except Exception:
        currency = None
    try:
        info = ticker.info or {}
        name = info.get("shortName") or info.get("longName") or symbol
        dividend = _dividend_yield(info)
        if currency is None:
            currency = info.get("currency")
    except Exception:
        info = {}
    closes = history["Close"].dropna()
    return store_history(symbol, market, closes, currency if isinstance(currency, str) else None, dividend, name)
