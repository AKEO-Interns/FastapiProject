from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.bookSchema import BookCreate
from app.loggerConfig.logger_config import LoggerService

logger_service = LoggerService(service="bookService")
def create_book(db: Session, book: BookCreate):
    new_book = Book(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    logger_service.log(
    "info",
    "Book created successfully",
    {"id": new_book.id, "title": new_book.title, "author": new_book.author}
    )
    return new_book

def get_all_books(db: Session):
    return db.query(Book).all()
