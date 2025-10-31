from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"routes": [str(rule) for rule in current_app.url_map.iter_rules()]})


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create access token
    access_token = create_access_token(identity=user.id)

    return (
        jsonify(
            {
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                },
            }
        ),
        200,
    )


# Signup route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "farmer")  # default role is farmer

    if not full_name or not email or not password:
        return jsonify({"error": "Full name, email, and password are required"}), 400

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create new user
    new_user = User(
        full_name=full_name, email=email, password=hashed_password, role=role
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {email} created successfully"}), 201
