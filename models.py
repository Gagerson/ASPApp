"""
models.py — Defines the SQLAlchemy database models.
"""

from datetime import datetime, UTC
from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique
    role = db.Column(db.String(10), nullable=False, default="regular")
    password_hash = db.Column(db.String(255), nullable=False)  # Stored as a hash

    def set_password(self, password: str) -> None:  # Hash and store the user password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(40), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_ref = db.Column(db.String(30), unique=True, nullable=False)

    robot_id = db.Column(db.Integer, db.ForeignKey("robot.id"), nullable=False)
    robot = db.relationship("Robot", backref=db.backref("tickets", lazy=True))

    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_by = db.relationship("User", foreign_keys=[created_by_user_id])

    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    assigned_to = db.relationship("User", foreign_keys=[assigned_to_user_id])

    category = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(30), nullable=False, default="New")
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class TicketUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)
    ticket = db.relationship(
        "Ticket",
        backref=db.backref("updates", lazy=True, cascade="all, delete-orphan")
    )

    updated_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    updated_by = db.relationship("User")

    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
