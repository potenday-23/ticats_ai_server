# built-in
import uuid
from datetime import datetime, timedelta

# fast-api
from app.config.config import redis_client


def create_session_id() -> str:
    """
    session id는 유일해야하며, 추측이 쉽지 않아야 하므로 UUID를 session id의 표준으로 한다.
    """
    return str(uuid.uuid4())


def save_session_to_redis(user_id: int) -> str:
    """
    redis에 session형식으로 저장 후 cache_id 반환
    - key : user::login::session_id
    - value : {
        "sessionId" : "6843f2dc-24fa-11e9-b84a-f8633f2431a4"
        "userId" : 10,
        "expiresAt" : 1209600
    }
    """

    # session 생성
    session_id = create_session_id()
    session_content = {
        "sessionId": session_id,
        "userId": user_id,
        "expiresAt": datetime.now() + timedelta(weeks=2)
    }

    # redis 저장
    redis_key = "user::login::" + session_id
    redis_client.set(redis_key, session_content.__str__(), 1209600)  # 2주

    return redis_key
