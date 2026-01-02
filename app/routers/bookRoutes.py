from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.schemas.bookSchema import BookCreate, BookResponse
from app.services.bookService import create_book, get_all_books
from app.auth.auth_handler import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookResponse)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@router.get("/", response_model=list[BookResponse])
def list_books(
    current_user: str = Depends(get_current_user),  # JWT check
    db: Session = Depends(get_db)
):
    return get_all_books(db)

