
from app import app
from models import User
from db import db
from tests.conftest import login_as


def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_user_can_register(client):
    response = client.post('/register', data={
        'name': 'Agata Lee',
        'email': 'agata@example.com',
        'password': 'Password123',
        'role': 'regular',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful' in response.data

    with app.app_context():
        user = User.query.filter_by(email='agata@example.com').first()
        assert user is not None
        assert user.role == 'regular'


def test_valid_login_redirects_to_tickets(client, regular_user):
    response = login_as(client, 'regular@example.com')
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data
    assert b'Tickets' in response.data


def test_invalid_login_shows_message(client, regular_user):
    response = client.post('/login', data={
        'email': 'regular@example.com',
        'password': 'WrongPassword',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_unauthenticated_user_redirected_to_login(client):
    response = client.get('/tickets', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
