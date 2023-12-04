# third-party
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest
# Fast-app
from app.models import User, Board
from app.schemas.board_schema import BoardRequestSchema
from app.schemas.user_schema import UserSignupRequestSchema
from app.services.board_service import create_board, delete_board_by_id
from app.services.post_service import delete_post_by_id
from app.services.user_service import create_user, delete_user_by_id

POST_ROUTER_PATH = "/api/posts"

# 게시글 정보
title = "About Soccer's Strategy"
content = "Soccer is very good sports to increase your health"


@pytest.fixture(scope="module")
def user(db: Session):
    user_request_schema = UserSignupRequestSchema(email="testemail@test.com",
                                                  password="testpassword",
                                                  full_name="testfullname")
    user = create_user(db, user_request_schema)
    yield user
    delete_user_by_id(db, user.id)


@pytest.fixture(scope="module")
def board(db: Session, user: User):
    board_request_schema = BoardRequestSchema(name="Book",
                                              public=True,
                                              user_id=user.id)
    board = create_board(db, board_request_schema)
    yield board
    delete_board_by_id(db, board.id)


def test_게시글생성(client: TestClient, db: Session) -> None:
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
    board_data = {
        "name": "Movie",
        "public": True,
    }
    board_json = client.post("/api/boards", json=board_data, headers={"Authorization": access_token}).json()

    # given
    post_data = {
        "title": "게시글1",
        "content": "내용1",
        "board_id": int(board_json["id"])
    }

    # when
    r = client.post(POST_ROUTER_PATH, json=post_data, headers={"Authorization": access_token})
    create_post = r.json()

    # then
    assert r.status_code == 200
    assert create_post["title"] == "게시글1"
    assert create_post["content"] == "내용1"
    assert create_post["board_id"] == int(board_json["id"])
