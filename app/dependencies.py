from database import SessionReadOnly

def get_db():
    db = SessionReadOnly()
    try:
        yield db
    finally:
        db.close()