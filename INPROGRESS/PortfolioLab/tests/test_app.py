from app import create_app


def test_home_create_analyse_and_save(tmp_path):
    client = create_app(tmp_path).test_client()
    home = client.get("/")
    assert home.status_code == 200
    assert b"Portfolio Lab" in home.data
    assert b"Educational tool only" in home.data

    created = client.post("/portfolios", follow_redirects=False)
    assert created.status_code == 302
    location = created.headers["Location"]
    page = client.get(location)
    assert page.status_code == 200
    assert b"Load the lesson mix" in page.data

    portfolio_id = location.rstrip("/").split("/")[-1]
    saved = client.put(
        f"/api/portfolio/{portfolio_id}",
        json={
            "name": "Shown piece",
            "market": "US",
            "window": "1y",
            "risk_free_rate": 0.04,
            "max_weight": 0.5,
            "include_cash": True,
            "cash_yield": 0.04,
            "cash_weight": None,
            "tickers": ["AAPL", "MSFT", "BND"],
            "weights": {"AAPL": 0.3, "MSFT": 0.3, "BND": 0.3},
            "strategy": "equal",
            "expected_return_overrides": {},
        },
    )
    assert saved.status_code == 200
    assert saved.get_json()["name"] == "Shown piece"

    analysed = client.post(
        "/api/analyse",
        json={
            "market": "US",
            "window": "1y",
            "risk_free_rate": 0.04,
            "max_weight": 0.5,
            "include_cash": True,
            "cash_yield": 0.04,
            "tickers": ["AAPL", "MSFT", "BND"],
            "weights": {},
            "strategy": "min_variance",
            "expected_return_overrides": {},
        },
    )
    body = analysed.get_json()
    assert analysed.status_code == 200
    assert body["ok"]
    assert abs(sum(body["math"]["component_risk"]) - body["math"]["volatility"]) < 1e-6

    blocked = client.post(
        "/api/analyse",
        json={
            "market": "US",
            "window": "1y",
            "risk_free_rate": 0.04,
            "max_weight": 0.2,
            "include_cash": False,
            "tickers": ["AAPL", "MSFT", "BND"],
            "weights": {},
            "strategy": "equal",
            "expected_return_overrides": {},
        },
    )
    assert blocked.status_code == 400
    assert "60%" in blocked.get_json()["error"]

    deleted = client.delete(f"/api/portfolio/{portfolio_id}")
    assert deleted.status_code == 200
    assert client.get(f"/api/portfolio/{portfolio_id}").status_code == 404
