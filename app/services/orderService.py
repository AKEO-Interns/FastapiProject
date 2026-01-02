from app.models.order import Order
from app.database.db import SessionLocal

def create_order(user_id: int, book_id: int):
    db = SessionLocal()
    order = Order(user_id=user_id, book_id=book_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    db.close()
    return order

def update_order_status(order_id: int, status: str):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    db.close()
    return order
