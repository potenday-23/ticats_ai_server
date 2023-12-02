# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest

# fast-api
from app.services.user_service import delete_user_by_id, verify_password

# 경로
USER_ROUTER_PATH = "/api/users"

# 사용자 정보
email = "emailtest@test.com"
password = "passwordtest"
full_name = "fullnametest"


def test_create_user(client: TestClient, db: Session) -> None:
    # given
    sign_up_data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }

    # when
    r = client.post(USER_ROUTER_PATH + "/signup", json=sign_up_data)
    sign_up_user = r.json()
    delete_user_by_id(db, sign_up_user["id"])

    # then
    assert r.status_code == 200
    assert sign_up_user["email"] == email
    assert verify_password(password, sign_up_user["password"]) == True
    assert sign_up_user["full_name"] == full_name
