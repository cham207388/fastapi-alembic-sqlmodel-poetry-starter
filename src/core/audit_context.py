# src/core/audit_context.py
import contextvars

current_user_email = contextvars.ContextVar("current_user_email", default=None)