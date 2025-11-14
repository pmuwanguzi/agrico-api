from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Livestock, Farm

livestock_bp = Blueprint("livestock", __name__, url_prefix="/livestock")


# Create a new livestock entry
@livestock_bp.route("/", methods=["POST"])
@jwt_required()
def create_livestock():
    data = request.get_json()
    farm_id = data.get("farm_id")
    animal_type = data.get("animal_type")
    quantity = data.get("quantity")
    purchase_date = data.get("purchase_date")
    health_status = data.get("health_status")

    if not farm_id or not animal_type or quantity is None:
        return jsonify({"error": "farm_id, animal_type, and quantity are required"}), 400

    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    new_livestock = Livestock(
        farm_id=farm_id,
        animal_type=animal_type,
        quantity=quantity,
        purchase_date=purchase_date,
        health_status=health_status
    )
    db.session.add(new_livestock)
    db.session.commit()

    return jsonify({"message": "Livestock created successfully", "id": new_livestock.id}), 201


# Get all livestock for a farm
@livestock_bp.route("/<int:farm_id>", methods=["GET"])
@jwt_required()
def list_livestock(farm_id):
    livestock_list = Livestock.query.filter_by(farm_id=farm_id).all()
    results = [
        {
            "id": l.id,
            "animal_type": l.animal_type,
            "quantity": l.quantity,
            "purchase_date": l.purchase_date,
            "health_status": l.health_status
        }
        for l in livestock_list
    ]
    return jsonify(results), 200


# Update livestock
@livestock_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_livestock(id):
    livestock = Livestock.query.get(id)
    if not livestock:
        return jsonify({"error": "Livestock not found"}), 404

    data = request.get_json()
    livestock.animal_type = data.get("animal_type", livestock.animal_type)
    livestock.quantity = data.get("quantity", livestock.quantity)
    livestock.purchase_date = data.get("purchase_date", livestock.purchase_date)
    livestock.health_status = data.get("health_status", livestock.health_status)

    db.session.commit()
    return jsonify({"message": "Livestock updated successfully"}), 200


# Delete livestock
@livestock_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_livestock(id):
    livestock = Livestock.query.get(id)
    if not livestock:
        return jsonify({"error": "Livestock not found"}), 404

    db.session.delete(livestock)
    db.session.commit()
    return jsonify({"message": "Livestock deleted successfully"}), 200