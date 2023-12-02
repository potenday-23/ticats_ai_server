# built-in
from typing import Generator
# third-party
from fastapi.testclient import TestClient
import pytest
# fast-api
from app.config.database import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c
