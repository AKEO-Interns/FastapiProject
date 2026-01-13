from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str  # raw password from request


class UserLogin(BaseModel):
    username: str
    password: str
    model_config = ConfigDict(extra="forbid")
   
class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}  # use ORM mode

