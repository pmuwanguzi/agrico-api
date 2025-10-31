from flask_jwt_extended import create_access_token


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)

    return (
        jsonify(
            {
                "message": f"Welcome back, {user.full_name}!",
                "access_token": access_token,
                "role": user.role,
            }
        ),
        200,
    )
