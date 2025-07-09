from datetime import datetime, timezone
from sqlalchemy import event
from sqlmodel import SQLModel
from src.core.audit_context import current_user_email
from loguru import logger

__event_registered = False  # ensures events are only registered once


def init_events():
    global __event_registered
    if __event_registered:
        logger.debug("🔁 Audit events already registered")
        return

    logger.info("✅ Registering SQLModel audit event listeners")
    __event_registered = True

    @event.listens_for(SQLModel, "before_update", propagate=True)
    def auto_update_audit_fields(mapper, connection, target):
        logger.debug(f"[AUDIT] before_update fired for {target}")
        fields = _audit_fields(target)
        now = datetime.now(timezone.utc)
        user = _get_current_user_email()
        logger.debug(f"[AUDIT] Updating fields with user={user}")

        match fields:
            case {"updated_at": _, "updated_by": _}:
                set_fields(target, updated_at=now, updated_by=user)
            case {"updated_at": _}:
                set_fields(target, updated_at=now)
            case {"updated_by": _}:
                set_fields(target, updated_by=user)

    @event.listens_for(SQLModel, "before_insert", propagate=True)
    def auto_insert_audit_fields(mapper, connection, target):
        logger.debug(f"[AUDIT] before_insert fired for {target}")
        fields = _audit_fields(target)
        now = datetime.now(timezone.utc)
        user = _get_current_user_email()

        # If no user is logged in, use the email of the user being created (if available)
        if user == "anonymous" and hasattr(target, "email"):
            user_email = getattr(target, "email", "anonymous")
        else:
            user_email = user

        match fields:
            case {"created_at": _, "updated_at": _, "created_by": _, "updated_by": _}:
                set_fields(
                    target,
                    created_at=now,
                    updated_at=now,
                    created_by=user_email,
                    updated_by=user_email
                )
            case _:
                for field in fields:
                    match field:
                        case "created_at" | "updated_at":
                            set_fields(target, **{field: now})
                        case "created_by" | "updated_by":
                            set_fields(target, **{field: user_email})


def _set_audit_field(target, field, value):
    try:
        setattr(target, field, value)
    except Exception as e:
        logger.warning(f"Failed to set audit field '{field}' on '{type(target).__name__}': {e}")


def set_fields(target, **fields):
    for field, value in fields.items():
        _set_audit_field(target, field, value)


def _get_current_user_email():
    email = current_user_email.get()
    return email if email else "anonymous"


def _audit_fields(target):
    return {
        field: getattr(target, field, None)
        for field in ("created_at", "updated_at", "created_by", "updated_by")
        if hasattr(target, field)
    }