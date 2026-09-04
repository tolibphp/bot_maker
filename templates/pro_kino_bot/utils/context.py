import contextvars

current_admin_id = contextvars.ContextVar("current_admin_id", default=0)
