# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest
# Fast-app
from app.models import User
from app.schemas.user_schema import UserSignupRequestSchema
from app.services.board_service import delete_board_by_id
from app.services.user_service import create_user, delete_user_by_id, delete_user_by_email

BOARD_ROUTER_PATH = "/api/boards"


def test_게시판_생성(client: TestClient, db: Session) -> None:
    # Setting
    sign_up_data = {
        "email": "test@test.com",
        "password": "Test",
        "full_name": "김가영"
    }
    client.post("/api/users/signup", json=sign_up_data)
    login_data = {
        "email": "test@test.com",
        "password": "Test",
    }
    r = client.post("/api/users/login", json=login_data)
    access_token = "Bearer " + r.headers["accesstoken"]

    # given
    board_data = {
        "name": "Movie",
        "public": True,
    }

    # when
    r = client.post(BOARD_ROUTER_PATH, json=board_data, headers={"Authorization": access_token})
    create_board = r.json()
    delete_user_by_email(db, "test@test.com")

    # then
    assert r.status_code == 200
    assert create_board["name"] == "Movie"
    assert create_board["public"] == True
