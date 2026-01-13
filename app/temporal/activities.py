from temporalio import activity
from app.database.db import SessionLocal
from app.services.bookService import get_all_books
from app.services.orderService import create_order
from temporalio.exceptions import ApplicationError
from app.auth.auth_handler import auth
@activity.defn
async def verify_user_activity(data: dict):
   

    token = data["token"]

    #  extract user_id FROM TOKEN (not payload)
    payload = auth.verify_jwt_token(token)
    if not payload:
        raise Exception("Invalid JWT")

    user_id = data.get("user_id")

    return {
        "verified": True,
        "user_id": user_id
    }  # include user_id

@activity.defn
async def check_inventory_activity(data: dict):
    book_id = data["book_id"]
    print(book_id)
    db = SessionLocal()
    try:
        books = get_all_books(db) 
        print(books)  # saari books fetch ho rahi hain
        for book in books:
            if book.id == book_id:  # agar match mil gaya
                return {"available": True, "book_id": book_id}
      
        return {"available": False, "book_id": book_id}
    finally:
        db.close()



@activity.defn
async def create_order_activity(data: dict):
    
    order = create_order(data["user_id"], data["book_id"])
    return {"order_id": order.id}

@activity.defn
async def apply_discount_activity(order:dict):
    """
    Applies discount in loop
    """
    order_id= order["order_id"]
    iteration = order.get("iteration", 0)
    print("apply discount :",order_id)
    discount = 5 * (iteration + 1)

    return {
        "order_id": order_id,
        "iteration": iteration,
        "discount_applied": discount
    }

@activity.defn
async def premium_offer_activity(order:dict):
    """
    Applies premium offer
    """
    order_id = order["order_id"]
    return {
        "order_id": order_id,
        "offer_type": "PREMIUM",
        "discount_percent": 25,
        "free_delivery": True
    }

@activity.defn
async def regular_offer_activity(order:dict):
    """
    Applies regular offer
    """
    order_id = order["order_id"]
    return {
        "order_id": order_id,
        "offer_type": "REGULAR",
        "discount_percent": 15,
        "free_delivery": False
    }

@activity.defn
async def basic_offer_activity(order: dict):
    """
    Applies basic/default offer
    """
    order_id = order["order_id"]
    print("basic offer activity: ",order_id)
    return {
        "order_id": order_id,
        "offer_type": "BASIC",
        "discount_percent": 5,
        "free_delivery": False
    }


@activity.defn
async def end_activity(data:dict):
    return {}




