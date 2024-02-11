import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Setup Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

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