# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest
# Fast-app
from app.models import User
from app.schemas.user_schema import UserSignupRequestSchema
from app.services.board_service import delete_board_by_id
from app.services.user_service import create_user, delete_user_by_id

BOARD_ROUTER_PATH = "/app/boards"

# 게시판 정보
name = "Movie"
public = True


@pytest.fixture(scope="module")
def user(db: Session):
    user_request_schema = UserSignupRequestSchema(email="testemail@test.com",
                                                  password="testpassword",
                                                  full_name="testfullname")
    user = create_user(db, user_request_schema)
    yield user
    delete_user_by_id(db, user.id)


def test_create_board(client: TestClient, db: Session, user: User) -> None:
    # given
    board_data = {
        "name": "Movie",
        "public": True,
        "user_id": user.id
    }

    # when
    r = client.post(BOARD_ROUTER_PATH, json=board_data)
    create_board = r.json()
    delete_board_by_id(db, create_board["id"])

    # then
    assert r.status_code == 200
    assert create_board["name"] == name
    assert create_board["public"] == public
    assert create_board["user_id"] == user.id
