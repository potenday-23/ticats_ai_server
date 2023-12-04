# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest
# fast-api
from app.services.user_service import delete_user_by_id, verify_password, delete_user_by_email

# 경로
USER_ROUTER_PATH = "/api/users"


def test_회원가입(client: TestClient, db: Session) -> None:
    # given
    sign_up_data = {
        "email": "test@test.com",
        "password": "Test",
        "full_name": "김가영"
    }

    # when
    r = client.post(USER_ROUTER_PATH + "/signup", json=sign_up_data)
    sign_up_user = r.json()
    delete_user_by_email(db, "test@test.com")

    # then
    assert r.status_code == 200
    assert sign_up_user["email"] == "test@test.com"
    assert sign_up_user["full_name"] == "김가영"


def test_로그인(client: TestClient, db: Session) -> None:
    # given
    sign_up_data = {
        "email": "test@test.com",
        "password": "Test",
        "full_name": "김가영"
    }
    client.post(USER_ROUTER_PATH + "/signup", json=sign_up_data)
    login_data = {
        "email": "test@test.com",
        "password": "Test",
    }

    # when
    r = client.post(USER_ROUTER_PATH + "/login", json=login_data)

    # then
    assert r.status_code == 204
    assert r.headers["accesstoken"]


def test_로그아웃(client: TestClient, db: Session) -> None:
    # given
    sign_up_data = {
        "email": "test@test.com",
        "password": "Test",
        "full_name": "김가영"
    }
    client.post(USER_ROUTER_PATH + "/signup", json=sign_up_data)
    login_data = {
        "email": "test@test.com",
        "password": "Test",
    }
    r = client.post(USER_ROUTER_PATH + "/login", json=login_data)
    accesstoken = r.headers["accesstoken"]

    # when
    client.post(USER_ROUTER_PATH + "/logout", headers={"Authorization": "Bearer " + accesstoken})
    delete_user_by_email(db, "test@test.com")

    # then
    assert r.status_code == 204
