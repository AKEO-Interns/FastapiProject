from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    price: float

class BookResponse(BookCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
