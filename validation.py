"""
validation.py — Input validation functions and the custom ValidationError exception class.
"""

from constants import TICKET_CATEGORIES, TICKET_STATUSES, ROBOT_PLATFORMS


class ValidationError(ValueError):
    pass


def validate_robot(name: str, platform: str) -> None:
    if not name.strip():  # Name must not be blank
        raise ValidationError("Robot name is required.")
    if platform not in ROBOT_PLATFORMS:  # Platform must match one of the allowed values defined in constants.py
        raise ValidationError("Platform must be UiPath or Power Automate.")


def validate_ticket(category: str, subject: str, description: str, status: str) -> None:
    if category not in TICKET_CATEGORIES:  # Category and status must match the allowed sets defined in constants.py
        raise ValidationError("Invalid category.")
    if status not in TICKET_STATUSES:
        raise ValidationError("Invalid status.")
    if len(subject.strip()) < 5:  # Subject and description must meet minimum length requirements
        raise ValidationError("Subject must be at least 5 characters.")
    if len(description.strip()) < 10:
        raise ValidationError("Description must be at least 10 characters.")


def validate_update(note: str) -> None:
    if not note.strip():
        raise ValidationError("Update note cannot be empty.")


def validate_registration(name: str, email: str, password: str, role: str) -> None:
    if len(name.strip()) < 2:  # Name must be at least 2 characters
        raise ValidationError("Name must be at least 2 characters.")
    if "@" not in email or "." not in email:  # Email format check — must contain @ and a dot
        raise ValidationError("Enter a valid email address.")
    if len(password) < 6:   # Password must be at least 6 characters
        raise ValidationError("Password must be at least 6 characters.")
    if role not in {"admin", "regular"}:
        raise ValidationError("Invalid role.")


def validate_login(email: str, password: str) -> None:  # Validate that email and password fields are not empty
    if not email.strip():
        raise ValidationError("Email is required.")
    if not password:
        raise ValidationError("Password is required.")
