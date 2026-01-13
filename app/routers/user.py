from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.userService import create_user, authenticate_user
from app.auth.auth_handler import auth
from app.models.user import User

from app.database.utils import soft_delete

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db) ):
    return create_user(db, user.username, user.password)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": str(db_user.id), 
                                      "username":db_user.username
                                      })
    return {"access_token": token, "token_type": "bearer"}

@router.delete("/delete/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    #  Fetch the user (only active users)
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Soft delete using reusable function
    soft_delete(db, user)

    return {"message": f"User with ID {user_id} soft deleted successfully"}
