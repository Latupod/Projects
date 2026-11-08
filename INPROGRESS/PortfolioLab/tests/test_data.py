import pandas as pd
import pytest

from portfolio_lab.data import UnknownTickerError, normalize_quote, resolve_prices, slice_window
from portfolio_lab.live import clean_symbol, store_history


def test_pence_quotes_convert_only_when_the_level_looks_like_pence():
    pence = pd.Series([2800.0, 2750.0, 2900.0])
    converted, currency, note = normalize_quote(pence, "GBp")
    assert currency == "GBP"
    assert converted.iloc[0] == pytest.approx(28.0)
    assert "pence" in note.lower()

    pounds = pd.Series([27.0, 28.0, 26.0])
    unchanged, currency, note = normalize_quote(pounds, "GBX")
    assert currency == "GBP"
    assert unchanged.iloc[0] == pytest.approx(27.0)
    assert "left unchanged" in note.lower()

    dollars, currency, note = normalize_quote(pd.Series([150.0, 151.0]), "USD")
    assert currency == "USD"
    assert note is None
    assert dollars.iloc[0] == pytest.approx(150.0)


def test_short_file_explains_that_the_window_was_shortened():
    index = pd.bdate_range("2024-01-02", periods=10)
    frame = pd.DataFrame({"A": range(100, 110)}, index=index)
    sliced, note = slice_window(frame, "5y")
    assert len(sliced) == 10
    assert "does not go back a full 5 years" in note


def test_unknown_ticker_and_symbol_safety(tmp_path, monkeypatch):
    with pytest.raises(UnknownTickerError):
        resolve_prices("US", "NOTREAL")
    with pytest.raises(ValueError):
        clean_symbol("../AAPL")
    with pytest.raises(ValueError):
        clean_symbol("AAPL/MSFT")
    assert clean_symbol("SHEL.L") == "SHEL.L"
    assert clean_symbol("^GSPC") == "^GSPC"

    monkeypatch.setattr("portfolio_lab.live.CACHE_DIR", tmp_path)
    series = pd.Series([2800.0, 2750.0], index=pd.to_datetime(["2024-01-02", "2024-01-03"]))
    meta = store_history("SHEL.L", "UK", series, "GBp", 0.03, "Shell")
    assert meta["currency"] == "GBP"
    saved = pd.read_csv(tmp_path / "UK" / "SHEL.L.csv")
    assert saved["close"].iloc[0] == pytest.approx(28.0)
