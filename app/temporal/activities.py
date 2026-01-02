from temporalio import activity
from app.database.db import SessionLocal
from app.services.bookService import get_all_books
from app.services.orderService import create_order
from temporalio.exceptions import ApplicationError

@activity.defn
async def verify_user_activity(data: dict):
    from app.auth.auth_handler import verify_jwt_token

    token = data["token"]
    if not verify_jwt_token(token):
        raise Exception("Invalid JWT")
    return {"verified": True}


@activity.defn
async def check_inventory_activity(data: dict):
    book_id = data["book_id"]
    db = SessionLocal()
    try:
        books = get_all_books(db)
        for book in books:
            if book.id == book_id:
                return {"available": True, "book_id": book_id}  # <-- include book_id
        raise ApplicationError(
            "Book not available",
            type="BOOK_OUT_OF_STOCK",
            non_retryable=True
        )
    finally:
        db.close()


@activity.defn
async def create_order_activity(data: dict):
 

    order = create_order(data["user_id"], data["book_id"])
    return {"order_id": order.id}

