
import pytest
from validation import (
    validate_robot,
    validate_ticket,
    validate_update,
    validate_registration,
    validate_login,
    ValidationError,
)


def test_validate_robot_accepts_valid_values():
    validate_robot('Complaints Bot', 'UiPath')


def test_validate_robot_rejects_invalid_platform():
    with pytest.raises(ValidationError):
        validate_robot('Complaints Bot', 'Blue Prism')


def test_validate_ticket_rejects_invalid_category():
    with pytest.raises(ValidationError):
        validate_ticket('BadCategory', 'Valid Subject', 'This is a valid description.', 'New')


def test_validate_ticket_rejects_short_subject():
    with pytest.raises(ValidationError):
        validate_ticket('Incident', 'Bad', 'This is a valid description.', 'New')


def test_validate_update_rejects_blank_note():
    with pytest.raises(ValidationError):
        validate_update('   ')


def test_validate_registration_rejects_short_password():
    with pytest.raises(ValidationError):
        validate_registration('Agata', 'agata@example.com', '123', 'regular')


def test_validate_login_rejects_empty_email():
    with pytest.raises(ValidationError):
        validate_login('', 'Password123')
