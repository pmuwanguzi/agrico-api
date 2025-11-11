from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Crop, Farm, User

crop_bp = Blueprint("crop_bp", __name__, url_prefix="/crops")


# Helper function to check admin role
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == "admin"


# CREATE a new crop (Admin only)
@crop_bp.route("/", methods=["POST"])
@jwt_required()
def create_crop():
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    farm_id = data.get("farm_id")
    crop_name = data.get("crop_name")
    crop_type = data.get("crop_type")
    planting_date = data.get("planting_date")
    harvest_date = data.get("harvest_date")
    expected_yield = data.get("expected_yield")

    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    new_crop = Crop(
        farm_id=farm_id,
        crop_name=crop_name,
        crop_type=crop_type,
        planting_date=planting_date,
        harvest_date=harvest_date,
        expected_yield=expected_yield
    )

    db.session.add(new_crop)
    db.session.commit()

    return jsonify({"message": "Crop created successfully", "crop_id": new_crop.crop_id}), 201


# LIST all crops (Admin only)
@crop_bp.route("/", methods=["GET"])
@jwt_required()
def list_crops():
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Admin access required"}), 403

    crops = Crop.query.all()
    result = [
        {
            "crop_id": c.crop_id,
            "farm_id": c.farm_id,
            "crop_name": c.crop_name,
            "crop_type": c.crop_type,
            "planting_date": c.planting_date,
            "harvest_date": c.harvest_date,
            "expected_yield": c.expected_yield
        }
        for c in crops
    ]
    return jsonify({"crops": result}), 200


# UPDATE a crop (Admin only)
@crop_bp.route("/<int:crop_id>", methods=["PUT"])
@jwt_required()
def update_crop(crop_id):
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Admin access required"}), 403

    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({"error": "Crop not found"}), 404

    data = request.get_json()
    crop.crop_name = data.get("crop_name", crop.crop_name)
    crop.crop_type = data.get("crop_type", crop.crop_type)
    crop.planting_date = data.get("planting_date", crop.planting_date)
    crop.harvest_date = data.get("harvest_date", crop.harvest_date)
    crop.expected_yield = data.get("expected_yield", crop.expected_yield)

    db.session.commit()
    return jsonify({"message": "Crop updated successfully"}), 200


# DELETE a crop (Admin only)
@crop_bp.route("/<int:crop_id>", methods=["DELETE"])
@jwt_required()
def delete_crop(crop_id):
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Admin access required"}), 403

    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({"error": "Crop not found"}), 404

    db.session.delete(crop)
    db.session.commit()
    return jsonify({"message": "Crop deleted successfully"}), 200
