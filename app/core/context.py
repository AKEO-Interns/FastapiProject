# app/core/context.py
from contextvars import ContextVar

current_user_ctx : ContextVar[int] =ContextVar("current_user_id", default=None)

