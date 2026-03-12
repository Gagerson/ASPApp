
from app import app
from db import db
from models import Ticket, TicketUpdate
from tests.conftest import login_as


def test_logged_in_user_can_create_ticket(client, regular_user, robot):
    login_as(client, 'regular@example.com')

    response = client.post('/tickets/add', data={
        'robot_id': str(robot),
        'assigned_to_id': '',
        'category': 'StatusCheck',
        'subject': 'Is the robot running?',
        'description': 'Please confirm whether the robot ran successfully today.',
        'status': 'New',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Ticket created successfully' in response.data
    assert b'Is the robot running?' in response.data

    with app.app_context():
        ticket = Ticket.query.first()
        assert ticket is not None
        assert ticket.created_by.email == 'regular@example.com'


def test_ticket_detail_adds_update_with_logged_in_user(client, regular_user, robot):
    login_as(client, 'regular@example.com')

    client.post('/tickets/add', data={
        'robot_id': str(robot),
        'assigned_to_id': '',
        'category': 'Incident',
        'subject': 'Report missing',
        'description': 'The expected robot report was not received this morning.',
        'status': 'New',
    }, follow_redirects=True)

    with app.app_context():
        ticket = Ticket.query.first()

    response = client.post(f'/tickets/{ticket.id}', data={
        'note': 'Investigating the missing report now.',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Update added' in response.data
    assert b'Investigating the missing report now.' in response.data

    with app.app_context():
        updates = TicketUpdate.query.filter_by(ticket_id=ticket.id).all()
        assert len(updates) == 2  # creation update + manual update
        assert updates[-1].updated_by.email == 'regular@example.com'


def test_regular_user_cannot_delete_ticket(client, regular_user, robot):
    login_as(client, 'regular@example.com')

    client.post('/tickets/add', data={
        'robot_id': str(robot),
        'assigned_to_id': '',
        'category': 'Incident',
        'subject': 'Delete test ticket',
        'description': 'Creating a ticket to verify delete permissions.',
        'status': 'New',
    }, follow_redirects=True)

    with app.app_context():
        ticket = Ticket.query.first()

    response = client.post(f'/tickets/{ticket.id}/delete', follow_redirects=False)
    assert response.status_code == 403


def test_admin_user_can_delete_ticket(client, admin_user, robot):
    login_as(client, 'admin@example.com')

    client.post('/tickets/add', data={
        'robot_id': str(robot),
        'assigned_to_id': '',
        'category': 'ChangeRequest',
        'subject': 'Delete me',
        'description': 'Creating a ticket to verify admin delete permissions.',
        'status': 'New',
    }, follow_redirects=True)

    with app.app_context():
        ticket = Ticket.query.first()
        assert ticket is not None
        ticket_id = ticket.id

    response = client.post(f'/tickets/{ticket_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Ticket deleted' in response.data

    with app.app_context():
        ticket = db.session.get(Ticket, ticket_id)
        assert ticket is None


def test_invalid_ticket_submission_shows_validation_message(client, regular_user, robot):
    login_as(client, 'regular@example.com')

    response = client.post('/tickets/add', data={
        'robot_id': str(robot),
        'assigned_to_id': '',
        'category': 'InvalidCategory',
        'subject': 'Bad',
        'description': 'Too short',
        'status': 'New',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid category' in response.data
