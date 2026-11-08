"""Named portfolios as JSON files. No accounts."""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from portfolio_lab.data import ROOT

PORTFOLIO_DIR = ROOT / "data" / "portfolios"
_ID = re.compile(r"^[a-f0-9]{32}$")

DEFAULTS = {
    "name": "New portfolio",
    "market": "US",
    "window": "3y",
    "risk_free_rate": 0.04,
    "max_weight": 0.40,
    "include_cash": True,
    "cash_yield": 0.04,
    "cash_weight": None,
    "tickers": [],
    "weights": {},
    "strategy": "user",
    "expected_return_overrides": {},
}


class PortfolioNotFound(LookupError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _check_id(portfolio_id: str) -> str:
    if not _ID.fullmatch(portfolio_id or ""):
        raise PortfolioNotFound("That portfolio does not exist.")
    return portfolio_id


class PortfolioStore:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else PORTFOLIO_DIR
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, portfolio_id: str) -> Path:
        return self.root / f"{_check_id(portfolio_id)}.json"

    def list_portfolios(self) -> list[dict]:
        found = []
        for path in self.root.glob("*.json"):
            if not _ID.fullmatch(path.stem):
                continue
            with path.open(encoding="utf-8") as handle:
                found.append(json.load(handle))
        found.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return found

    def get(self, portfolio_id: str) -> dict:
        path = self._path(portfolio_id)
        if not path.exists():
            raise PortfolioNotFound("That portfolio does not exist.")
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def create(self, payload: dict | None = None) -> dict:
        portfolio_id = uuid.uuid4().hex
        document = dict(DEFAULTS)
        if payload:
            document.update(_editable(payload))
        document["id"] = portfolio_id
        document["created_at"] = _now()
        document["updated_at"] = document["created_at"]
        self._write(document)
        return document

    def update(self, portfolio_id: str, payload: dict) -> dict:
        current = self.get(portfolio_id)
        current.update(_editable(payload))
        current["id"] = portfolio_id
        current["updated_at"] = _now()
        self._write(current)
        return current

    def delete(self, portfolio_id: str) -> None:
        path = self._path(portfolio_id)
        if not path.exists():
            raise PortfolioNotFound("That portfolio does not exist.")
        path.unlink()

    def _write(self, document: dict) -> None:
        path = self._path(document["id"])
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")


def _editable(payload: dict) -> dict:
    """Keep only the fields a saved portfolio is allowed to store. Prices are not copied."""
    if not isinstance(payload, dict):
        raise ValueError("The portfolio must be a JSON object.")
    name = str(payload.get("name") or "New portfolio").strip()[:80] or "New portfolio"
    market = payload.get("market", "US")
    if market not in {"US", "UK"}:
        raise ValueError("Choose the US market or the UK market.")
    window = payload.get("window", "3y")
    if window not in {"1y", "3y", "5y", "all"}:
        raise ValueError("Window must be 1y, 3y, 5y, or all.")
    strategy = payload.get("strategy", "user")
    if strategy not in {"user", "equal", "min_variance", "max_sharpe", "growth"}:
        raise ValueError("Unknown strategy.")
    tickers = []
    for ticker in payload.get("tickers") or []:
        text = str(ticker).strip()
        if text and text not in tickers and text != "CASH":
            tickers.append(text)
    if len(tickers) > 12:
        raise ValueError("Choose 12 holdings or fewer so the covariance matrix stays readable.")
    weights = payload.get("weights") or {}
    if not isinstance(weights, dict):
        raise ValueError("Weights must be an object of ticker to weight.")
    overrides = payload.get("expected_return_overrides") or {}
    if not isinstance(overrides, dict):
        raise ValueError("Expected-return overrides must be an object of ticker to return.")
    cash_weight = payload.get("cash_weight", None)
    if cash_weight is not None and cash_weight != "":
        cash_weight = float(cash_weight)
    else:
        cash_weight = None
    return {
        "name": name,
        "market": market,
        "window": window,
        "risk_free_rate": float(payload.get("risk_free_rate", 0.04)),
        "max_weight": float(payload.get("max_weight", 0.40)),
        "include_cash": bool(payload.get("include_cash", False)),
        "cash_yield": float(payload.get("cash_yield", 0.04)),
        "cash_weight": cash_weight,
        "tickers": tickers,
        "weights": {str(key): float(value) for key, value in weights.items() if str(key) != "CASH"},
        "strategy": strategy,
        "expected_return_overrides": {
            str(key): float(value) for key, value in overrides.items() if value is not None and str(key) != "CASH"
        },
    }
