
import os
import sys
import tempfile
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
from db import db
from models import User, Robot, Ticket, TicketUpdate


@pytest.fixture()
def client():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    with app.app_context():
        db.session.remove()
        try:
            db.engine.dispose()
        except Exception:
            pass
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()
        try:
            db.engine.dispose()
        except Exception:
            pass

    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture()
def admin_user(client):
    with app.app_context():
        user = User(name='Admin User', email='admin@example.com', role='admin')
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def regular_user(client):
    with app.app_context():
        user = User(name='Regular User', email='regular@example.com', role='regular')
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def robot(client):
    with app.app_context():
        robot = Robot(name='Complaints Bot', platform='UiPath', is_active=True)
        db.session.add(robot)
        db.session.commit()
        return robot.id


def login_as(client, email, password='Password123'):
    return client.post('/login', data={
        'email': email,
        'password': password,
    }, follow_redirects=True)
