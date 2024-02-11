import pytest
from flask import session
from app.app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import User

# Setup and teardown for each test function
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_user_registration(client):
    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ))
    assert response.status_code == 200
    assert b"User registered successfully" in response.data

def test_user_login(client):
    # Create a user first
    user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ))
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_login_wrong_password(client):
    # Create a user first
    user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data=dict(
        username='testuser',
        password='wrongpassword'
    ))
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_login_session(client):
    # Create a user and log in
    user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ))
        assert response.status_code == 200
        assert session['user_id'] == user.id  # Check if user_id is in session

def test_logout_session(client):
    # Create a user and log in, then log out
    user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
    db.session.add(user)
    db.session.commit()

    with client:
        client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = client.post('/logout')
        assert response.status_code == 200
        assert 'user_id' not in session  # Check if user_id is not in session
