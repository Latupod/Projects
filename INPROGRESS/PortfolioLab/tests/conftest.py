import pytest

from portfolio_lab.synthetic import build_fixtures


@pytest.fixture(scope="session", autouse=True)
def sample_fixtures():
    build_fixtures()
