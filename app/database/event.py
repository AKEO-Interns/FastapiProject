# app/database/events.py

from sqlalchemy import event
from sqlalchemy.orm import Session
from app.core.context import current_user_ctx

@event.listens_for(Session, "before_flush")
def set_audit_fields(session, flush_context, instances):
    user_id = current_user_ctx.get()
    print(user_id)
    if not user_id:
        return

    for obj in session.new:
        if hasattr(obj, "created_by"):
            obj.created_by = user_id
            obj.updated_by = user_id

    for obj in session.dirty:
        if hasattr(obj, "updated_by"):
            obj.updated_by = user_id
