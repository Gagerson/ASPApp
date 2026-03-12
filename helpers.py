"""
helpers.py — Utility functions for ticket reference generation and authentication.
"""
from datetime import datetime, UTC
from models import Ticket
from functools import wraps
from flask import session, redirect, url_for, abort


def generate_ticket_ref() -> str:  # Generate a unique ticket reference in the format AUTO-YYYY-NNNN
    year = datetime.now(UTC).year
    prefix = f"AUTO-{year}-"
    last = Ticket.query.filter(Ticket.ticket_ref.like(f"{prefix}%")).order_by(Ticket.id.desc()).first()
    if not last:
        return f"{prefix}0001"
    last_num = int(last.ticket_ref.split("-")[-1])
    return f"{prefix}{last_num + 1:04d}"


def login_required(view_func):  # redirect unauthenticated users to the login page
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


def admin_required(view_func):  # route for admin users only
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        if session.get("user_role") != "admin":
            abort(403)

        return view_func(*args, **kwargs)

    return wrapper
