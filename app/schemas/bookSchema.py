from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    price: float

class BookResponse(BookCreate):
    id: int
    title: str
    author: str
    price: float

    # model_config = {
    #     "from_attributes": True
    # }
