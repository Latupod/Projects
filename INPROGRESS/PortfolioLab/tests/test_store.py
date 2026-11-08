import pytest

from portfolio_lab.store import PortfolioNotFound, PortfolioStore


def test_portfolios_round_trip_without_storing_prices(tmp_path):
    store = PortfolioStore(tmp_path)
    created = store.create({"name": "Lesson", "market": "US", "tickers": ["AAPL", "BND"], "max_weight": 1})
    assert created["id"]
    assert store.get(created["id"])["tickers"] == ["AAPL", "BND"]
    store.update(created["id"], {**created, "name": "Renamed", "expected_return_overrides": {"AAPL": 0.08}})
    loaded = store.get(created["id"])
    assert loaded["name"] == "Renamed"
    assert loaded["expected_return_overrides"]["AAPL"] == pytest.approx(0.08)
    raw = (tmp_path / f"{created['id']}.json").read_text(encoding="utf-8")
    assert "close" not in raw
    assert "covariance" not in raw
    store.delete(created["id"])
    with pytest.raises(PortfolioNotFound):
        store.get(created["id"])


def test_portfolio_ids_cannot_escape_the_folder(tmp_path):
    store = PortfolioStore(tmp_path)
    with pytest.raises(PortfolioNotFound):
        store.get("../secret")
