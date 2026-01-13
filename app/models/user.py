from sqlalchemy import Column, Integer, String
from app.database.base import Base
from app.models.auditlog import AuditBase

class User(Base, AuditBase):
    __tablename__ = "users"
     
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
