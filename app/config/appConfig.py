from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str = Field(..., min_length=10)
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES :int

    class Config:
        env_file = ".env"   # load from .env file

Settings = Settings() 