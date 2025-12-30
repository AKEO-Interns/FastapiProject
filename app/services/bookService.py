from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.bookSchema import BookCreate

def create_book(db: Session, book: BookCreate):
    new_book = Book(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.query(Book).all()
