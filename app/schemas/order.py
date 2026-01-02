from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    book_id: int
    user_email: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str
