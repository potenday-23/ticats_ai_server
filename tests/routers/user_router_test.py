# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest

# fast-app
from app.services.user_service import delete_user_by_id

# 경로
USER_ROUTER_PATH = "/app/users"

# 사용자 정보
email = "emailtest@exampletest.com"
password = "passwordtest"
full_name = "fullnametest"


# todo : 비밀번호 인코딩시 assert문을 바꿔주어야 함
def test_create_user(client: TestClient, db: Session) -> None:
    # given
    sign_up_data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }

    # when
    r = client.post(USER_ROUTER_PATH + "/sign-up", json=sign_up_data)
    sign_up_user = r.json()

    # then
    assert r.status_code == 200
    assert sign_up_user["email"] == email
    assert sign_up_user["password"] == password
    assert sign_up_user["full_name"] == full_name

    # After
    delete_user_by_id(db, sign_up_user["id"])
