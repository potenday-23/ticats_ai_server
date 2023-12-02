# built-in
from typing import Generator
# third-party
from fastapi.testclient import TestClient
import pytest
# fast-api
from api.config.database_config import SessionLocal
from api.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c
