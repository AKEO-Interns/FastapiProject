from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth_handler import hash_password, verify_password

def create_user(db: Session, username: str, password: str):
    user = User(
        username=username,
        hashed_password=hash_password(password)  # matches model
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # matches model
        return None
    return user

