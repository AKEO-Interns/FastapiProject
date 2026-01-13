# app/models/auditlog.py
from sqlalchemy import Column, DateTime, Boolean, Integer
from sqlalchemy.sql import func

class AuditBase:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, server_default="false", nullable=False)