# from flask import Blueprint, request, jsonify
# from app import db
# from app.models import Farm, User
# from flask_jwt_extended import jwt_required, get_jwt_identity
#
# farm_bp = Blueprint("farm", __name__, url_prefix="/farms")
#
#
# # Helper to check admin role
# def admin_required():
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)
#     if not user or user.role != "admin":
#         return False, jsonify({"error": "Admin access required"}), 403
#     return True, user
#
#
# # POST /farms/
# @farm_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_farm():
#     is_admin, user_or_resp = admin_required()
#     if not is_admin:
#         return user_or_resp
#
#     data = request.get_json()
#     if not data.get("farm_name"):
#         return jsonify({"error": "farm_name is required"}), 400
#
#     farm = Farm(
#         farm_name=data["farm_name"],
#         location=data.get("location"),
#         size_acres=data.get("size_acres"),
#         user_id=user_or_resp.id,
#     )
#     db.session.add(farm)
#     db.session.commit()
#     return jsonify({"message": "Farm created successfully"}), 201
#
#
# # GET /farms/
# @farm_bp.route("/", methods=["GET"])
# @jwt_required()
# def list_farms():
#     is_admin, user_or_resp = admin_required()
#     if not is_admin:
#         return user_or_resp
#
#     farms = Farm.query.all()
#     farms_list = [
#         {
#             "farm_id": f.farm_id,
#             "farm_name": f.farm_name,
#             "location": f.location,
#             "size_acres": f.size_acres,
#         }
#         for f in farms
#     ]
#     return jsonify({"farms": farms_list}), 200
#
#
# # PUT /farms/<farm_id>
# @farm_bp.route("/<int:farm_id>", methods=["PUT"])
# @jwt_required()
# def update_farm(farm_id):
#     is_admin, user_or_resp = admin_required()
#     if not is_admin:
#         return user_or_resp
#
#     farm = Farm.query.get(farm_id)
#     if not farm:
#         return jsonify({"error": "Farm not found"}), 404
#
#     data = request.get_json()
#     farm.farm_name = data.get("farm_name", farm.farm_name)
#     farm.location = data.get("location", farm.location)
#     farm.size_acres = data.get("size_acres", farm.size_acres)
#     db.session.commit()
#     return jsonify({"message": "Farm updated successfully"}), 200
#
#
# # DELETE /farms/<farm_id>
# @farm_bp.route("/<int:farm_id>", methods=["DELETE"])
# @jwt_required()
# def delete_farm(farm_id):
#     is_admin, user_or_resp = admin_required()
#     if not is_admin:
#         return user_or_resp
#
#     farm = Farm.query.get(farm_id)
#     if not farm:
#         return jsonify({"error": "Farm not found"}), 404
#
#     db.session.delete(farm)
#     db.session.commit()
#     return jsonify({"message": "Farm deleted successfully"}), 200

from flask import Blueprint, request, jsonify
from app import db
from app.models import Farm, User
from flask_jwt_extended import jwt_required, get_jwt_identity

farm_bp = Blueprint("farm", __name__, url_prefix="/farms")


# ------------------ CREATE FARM ------------------
# POST /farms/
@farm_bp.route("/", methods=["POST"])
@jwt_required()
def create_farm():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data.get("farm_name"):
        return jsonify({"error": "farm_name is required"}), 400

    # Optional: check if user already has a farm
    existing_farm = Farm.query.filter_by(user_id=user.id).first()
    if existing_farm:
        return jsonify({"error": "User already has a farm"}), 400

    farm = Farm(
        farm_name=data["farm_name"],
        location=data.get("location"),
        size_acres=data.get("size_acres"),
        user_id=user.id,
    )
    db.session.add(farm)
    db.session.commit()

    return jsonify({
        "message": "Farm created successfully",
        "farm": {
            "farm_id": farm.farm_id,
            "farm_name": farm.farm_name,
            "location": farm.location,
            "size_acres": farm.size_acres
        }
    }), 201


# ------------------ LIST FARMS ------------------
# GET /farms/
@farm_bp.route("/", methods=["GET"])
@jwt_required()
def list_farms():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Only return farms belonging to this user
    farms = Farm.query.filter_by(user_id=user.id).all()
    farms_list = [
        {
            "farm_id": f.farm_id,
            "farm_name": f.farm_name,
            "location": f.location,
            "size_acres": f.size_acres,
        }
        for f in farms
    ]
    return jsonify({"farms": farms_list}), 200


# ------------------ UPDATE FARM ------------------
# PUT /farms/<farm_id>
@farm_bp.route("/<int:farm_id>", methods=["PUT"])
@jwt_required()
def update_farm(farm_id):
    current_user_id = get_jwt_identity()
    farm = Farm.query.get(farm_id)

    if not farm or farm.user_id != current_user_id:
        return jsonify({"error": "Farm not found or access denied"}), 404

    data = request.get_json()
    farm.farm_name = data.get("farm_name", farm.farm_name)
    farm.location = data.get("location", farm.location)
    farm.size_acres = data.get("size_acres", farm.size_acres)
    db.session.commit()

    return jsonify({"message": "Farm updated successfully"}), 200


# ------------------ DELETE FARM ------------------
# DELETE /farms/<farm_id>
@farm_bp.route("/<int:farm_id>", methods=["DELETE"])
@jwt_required()
def delete_farm(farm_id):
    current_user_id = get_jwt_identity()
    farm = Farm.query.get(farm_id)

    if not farm or farm.user_id != current_user_id:
        return jsonify({"error": "Farm not found or access denied"}), 404

    db.session.delete(farm)
    db.session.commit()

    return jsonify({"message": "Farm deleted successfully"}), 200


