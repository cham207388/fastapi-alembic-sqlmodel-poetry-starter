from datetime import datetime, timezone
from sqlalchemy import event
from sqlmodel import SQLModel
from src.core.audit_context import current_user_email


@event.listens_for(SQLModel, "before_update", propagate=True)
def auto_update_audit_fields(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)
    if hasattr(target, "updated_by"):
        target.updated_by = current_user_email.get()


@event.listens_for(SQLModel, "before_insert", propagate=True)
def auto_insert_audit_fields(mapper, connection, target):
    if hasattr(target, "created_at"):
        target.created_at = datetime.now(timezone.utc)
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)
    if hasattr(target, "created_by"):
        target.created_by = current_user_email.get()
    if hasattr(target, "updated_by"):
        target.updated_by = current_user_email.get()
