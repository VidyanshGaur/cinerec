import pytest
import sys
import os
sys.path.insert(0, '/Users/vidyansh/Desktop/recommendation-engine')

from backend.app import create_app
from backend.models import db, User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# TC-01: Valid Registration
def test_register_valid(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

# TC-02: Duplicate Email
def test_register_duplicate_email(client):
    client.post('/register', data={
        'name': 'User1',
        'email': 'dup@test.com',
        'password': 'password123'
    })
    response = client.post('/register', data={
        'name': 'User2',
        'email': 'dup@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'already registered' in response.data

# TC-03: Valid Login
def test_login_valid(client):
    client.post('/register', data={
        'name': 'Test User',
        'email': 'login@test.com',
        'password': 'password123'
    })
    response = client.post('/login', data={
        'email': 'login@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

# TC-04: Invalid Login
def test_login_invalid(client):
    response = client.post('/login', data={
        'email': 'wrong@test.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Invalid' in response.data

# TC-05: Unauthenticated access to dashboard
def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302