"""Laptop UI for Portfolio Lab. Run with: python app.py"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

from portfolio_lab.analysis import analyse
from portfolio_lab.data import UnknownTickerError, list_assets, market_info
from portfolio_lab.live import fetch_to_cache
from portfolio_lab.optimize import InfeasibleError
from portfolio_lab.store import PortfolioNotFound, PortfolioStore


def create_app(portfolio_dir: Path | None = None) -> Flask:
    app = Flask(__name__)
    store = PortfolioStore(portfolio_dir)

    @app.get("/")
    def home():
        return render_template("index.html", portfolios=store.list_portfolios())

    @app.post("/portfolios")
    def create_portfolio():
        document = store.create()
        return redirect(url_for("workspace", portfolio_id=document["id"]))

    @app.get("/portfolio/<portfolio_id>")
    def workspace(portfolio_id: str):
        try:
            store.get(portfolio_id)
        except PortfolioNotFound:
            return redirect(url_for("home"))
        return render_template("workspace.html", portfolio_id=portfolio_id)

    @app.get("/api/portfolio/<portfolio_id>")
    def api_get_portfolio(portfolio_id: str):
        try:
            return jsonify(store.get(portfolio_id))
        except PortfolioNotFound as exc:
            return jsonify(ok=False, error=str(exc)), 404

    @app.put("/api/portfolio/<portfolio_id>")
    def api_update_portfolio(portfolio_id: str):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(ok=False, error="Send a JSON object."), 400
        try:
            return jsonify(store.update(portfolio_id, payload))
        except PortfolioNotFound as exc:
            return jsonify(ok=False, error=str(exc)), 404
        except (TypeError, ValueError) as exc:
            return jsonify(ok=False, error=str(exc)), 400

    @app.delete("/api/portfolio/<portfolio_id>")
    def api_delete_portfolio(portfolio_id: str):
        try:
            store.delete(portfolio_id)
        except PortfolioNotFound as exc:
            return jsonify(ok=False, error=str(exc)), 404
        return jsonify(ok=True)

    @app.get("/api/universe/<market>")
    def api_universe(market: str):
        try:
            info = market_info(market)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        return jsonify(
            {
                "market": market,
                "currency": info["currency"],
                "currency_label": info["currency_label"],
                "benchmark": info["benchmark"],
                "assets": list_assets(market),
            }
        )

    @app.post("/api/analyse")
    def api_analyse():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(ok=False, error="Send a JSON object."), 400
        try:
            return jsonify(analyse(payload))
        except (InfeasibleError, UnknownTickerError, ValueError) as exc:
            return jsonify(ok=False, error=str(exc)), 400

    @app.post("/api/live")
    def api_live():
        payload = request.get_json(silent=True) or {}
        try:
            meta = fetch_to_cache(str(payload.get("symbol", "")), str(payload.get("market", "US")))
        except (LookupError, RuntimeError, ValueError) as exc:
            return jsonify(ok=False, error=str(exc)), 400
        return jsonify(ok=True, asset=meta)

    @app.get("/favicon.ico")
    def favicon():
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5050, debug=True)
