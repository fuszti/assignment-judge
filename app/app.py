import os

from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = os.urandom(24)  # or a static secret key for development
db = SQLAlchemy(app)


class User(db.Model):
    """
    User class represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)


@app.route("/register", methods=["POST"])
def register() -> tuple:
    """
    Register a new user.

    This function is used to register a new user in the application. It receives a POST request with the
    username and password in the request form. The password is hashed using the generate_password_hash
    function from the werkzeug.security module. The user is then created with the provided username and
    hashed password, and added to the database session. Finally, the changes are committed to the database.

    Returns:
        A JSON response with a success message and a status code of 200.
    """
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully."}), 200


@app.route("/login", methods=["POST"])
def login() -> tuple:
    """
    Login function for the Flask application.

    Parameters:
        None

    Returns:
        A JSON response containing a success message and status code 200 if the login is
        successful. A JSON response containing an error message and status code 401 if the
        credentials are invalid.
    """
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id  # Store user ID in session
        return jsonify({"message": "Login successful."}), 200
    return jsonify({"message": "Invalid credentials."}), 401


@app.route("/logout", methods=["POST"])
def logout() -> tuple:
    """
    Logout function.

    Removes the 'user_id' from the session, effectively logging out the user.

    Returns:
        A JSON response with a success message and a status code of 200.
    """
    session.pop("user_id", None)  # Remove user_id from session
    return jsonify({"message": "Logout successful."}), 200


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
