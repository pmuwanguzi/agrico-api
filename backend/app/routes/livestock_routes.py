# # from flask import Blueprint, request, jsonify
# # from flask_jwt_extended import jwt_required
# # from app import db
# # from app.models import Livestock, Farm
# #
# # livestock_bp = Blueprint("livestock", __name__, url_prefix="/livestock")
# #
# #
# # # Create a new livestock entry
# # @livestock_bp.route("/", methods=["POST"])
# # @jwt_required()
# # def create_livestock():
# #     data = request.get_json()
# #     farm_id = data.get("farm_id")
# #     animal_type = data.get("animal_type")
# #     quantity = data.get("quantity")
# #     purchase_date = data.get("purchase_date")
# #     health_status = data.get("health_status")
# #
# #     if not farm_id or not animal_type or quantity is None:
# #         return jsonify({"error": "farm_id, animal_type, and quantity are required"}), 400
# #
# #     farm = Farm.query.get(farm_id)
# #     if not farm:
# #         return jsonify({"error": "Farm not found"}), 404
# #
# #     new_livestock = Livestock(
# #         farm_id=farm_id,
# #         animal_type=animal_type,
# #         quantity=quantity,
# #         purchase_date=purchase_date,
# #         health_status=health_status
# #     )
# #     db.session.add(new_livestock)
# #     db.session.commit()
# #
# #     return jsonify({"message": "Livestock created successfully", "id": new_livestock.id}), 201
# #
# #
# # # Get all livestock for a farm
# # @livestock_bp.route("/<int:farm_id>", methods=["GET"])
# # @jwt_required()
# # def list_livestock(farm_id):
# #     livestock_list = Livestock.query.filter_by(farm_id=farm_id).all()
# #     results = [
# #         {
# #             "id": l.id,
# #             "animal_type": l.animal_type,
# #             "quantity": l.quantity,
# #             "purchase_date": l.purchase_date,
# #             "health_status": l.health_status
# #         }
# #         for l in livestock_list
# #     ]
# #     return jsonify(results), 200
# #
# #
# # # Update livestock
# # @livestock_bp.route("/<int:id>", methods=["PUT"])
# # @jwt_required()
# # def update_livestock(id):
# #     livestock = Livestock.query.get(id)
# #     if not livestock:
# #         return jsonify({"error": "Livestock not found"}), 404
# #
# #     data = request.get_json()
# #     livestock.animal_type = data.get("animal_type", livestock.animal_type)
# #     livestock.quantity = data.get("quantity", livestock.quantity)
# #     livestock.purchase_date = data.get("purchase_date", livestock.purchase_date)
# #     livestock.health_status = data.get("health_status", livestock.health_status)
# #
# #     db.session.commit()
# #     return jsonify({"message": "Livestock updated successfully"}), 200
# #
# #
# # # Delete livestock
# # @livestock_bp.route("/<int:id>", methods=["DELETE"])
# # @jwt_required()
# # def delete_livestock(id):
# #     livestock = Livestock.query.get(id)
# #     if not livestock:
# #         return jsonify({"error": "Livestock not found"}), 404
# #
# #     db.session.delete(livestock)
# #     db.session.commit()
# #     return jsonify({"message": "Livestock deleted successfully"}), 200
#
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import db
# from app.models import Livestock, Farm, User
#
# livestock_bp = Blueprint("livestock", __name__, url_prefix="/livestock")
#
# # ---------------- Helper ----------------
# # def user_owns_farm(farm_id: int, user_id: int):
# #     farm = Farm.query.get(farm_id)
# #     if not farm:
# #         return False, jsonify({"error": "Farm not found"}), 404
# #     if farm.user_id != user_id:
# #         return False, jsonify({"error": "You do not own this farm"}), 403
# #     return True, farm
# def user_owns_farm(farm_id, user_id):
#     farm = Farm.query.get(farm_id)
#     if not farm:
#         return False, {"error": "Farm not found"}  # only 2 values
#     if farm.user_id != user_id:
#         print(farm )
#         return False, {"error": "Unauthorized"}  # only 2 values
#     return True, farm
# # ---------------- Create ----------------
# @livestock_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_livestock():
#     current_user_id = get_jwt_identity()
#     data = request.get_json()
#     # print(data)
#     # print(current_user_id)
#
#     farm_id = data.get("farm_id")
#     animal_type = data.get("animal_type")
#     quantity = data.get("quantity")
#     purchase_date = data.get("purchase_date")
#     health_status = data.get("health_status")
#
#     if not farm_id or not animal_type or quantity is None:
#         return jsonify({"error": "farm_id, animal_type, and quantity are required"}), 400
#
#     valid, farm_or_resp = user_owns_farm(farm_id, current_user_id)
#     if not valid:
#         return farm_or_resp
#
#     new_livestock = Livestock(
#         farm_id=farm_id,
#         animal_type=animal_type,
#         quantity=quantity,
#         purchase_date=purchase_date,
#         health_status=health_status
#     )
#     db.session.add(new_livestock)
#     db.session.commit()
#
#     return jsonify({"message": "Livestock created successfully", "id": new_livestock.id}), 201
#
# # ---------------- List ----------------
# @livestock_bp.route("/", methods=["GET"])
# @jwt_required()
# def list_livestock():
#     current_user_id = get_jwt_identity()
#     # Get all farms of this user
#     farms = Farm.query.filter_by(user_id=current_user_id).all()
#     farm_ids = [f.farm_id for f in farms]
#
#     livestock_list = Livestock.query.filter(Livestock.farm_id.in_(farm_ids)).all()
#     results = [
#         {
#             "id": l.id,
#             "farm_id": l.farm_id,
#             "animal_type": l.animal_type,
#             "quantity": l.quantity,
#             "purchase_date": l.purchase_date,
#             "health_status": l.health_status
#         }
#         for l in livestock_list
#     ]
#     return jsonify(results), 200
#
# # ---------------- Update ----------------
# @livestock_bp.route("/<int:id>", methods=["PUT"])
# @jwt_required()
# def update_livestock(id):
#     current_user_id = get_jwt_identity()
#     livestock = Livestock.query.get(id)
#     if not livestock:
#         return jsonify({"error": "Livestock not found"}), 404
#
#     valid, farm_or_resp = user_owns_farm(livestock.farm_id, current_user_id)
#     if not valid:
#         return farm_or_resp
#
#     data = request.get_json()
#     livestock.animal_type = data.get("animal_type", livestock.animal_type)
#     livestock.quantity = data.get("quantity", livestock.quantity)
#     livestock.purchase_date = data.get("purchase_date", livestock.purchase_date)
#     livestock.health_status = data.get("health_status", livestock.health_status)
#
#     db.session.commit()
#     return jsonify({"message": "Livestock updated successfully"}), 200
#
# # ---------------- Delete ----------------
# @livestock_bp.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
# def delete_livestock(id):
#     current_user_id = get_jwt_identity()
#     livestock = Livestock.query.get(id)
#     if not livestock:
#         return jsonify({"error": "Livestock not found"}), 404
#
#     valid, farm_or_resp = user_owns_farm(livestock.farm_id, current_user_id)
#     if not valid:
#         return farm_or_resp
#
#     db.session.delete(livestock)
#     db.session.commit()
#     return jsonify({"message": "Livestock deleted successfully"}), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Livestock, Farm

livestock_bp = Blueprint("livestock", __name__, url_prefix="/livestock")


# Helper to get farms for a user
def get_user_farms(user_id):
    return Farm.query.filter_by(user_id=user_id).all()


# CREATE a new livestock entry
@livestock_bp.route("/", methods=["POST"])
@jwt_required()
def create_livestock():
    user_id = get_jwt_identity()
    data = request.get_json()
    farm_id = data.get("farm_id")

    if not farm_id:
        return jsonify({"error": "farm_id is required"}), 400

    # Check that farm belongs to the user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found or not linked to the user"}), 404

    animal_type = data.get("animal_type")
    quantity = data.get("quantity")
    purchase_date = data.get("purchase_date")
    health_status = data.get("health_status")

    if not animal_type or quantity is None:
        return jsonify({"error": "animal_type and quantity are required"}), 400

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


# LIST all livestock for user's farms
@livestock_bp.route("/", methods=["GET"])
@jwt_required()
def list_livestock():
    user_id = get_jwt_identity()
    farms = get_user_farms(user_id)
    if not farms:
        return jsonify({"livestock": []}), 200

    farm_ids = [f.farm_id for f in farms]
    livestock_list = Livestock.query.filter(Livestock.farm_id.in_(farm_ids)).all()

    results = [
        {
            "id": l.id,
            "farm_id": l.farm_id,
            "animal_type": l.animal_type,
            "quantity": l.quantity,
            "purchase_date": l.purchase_date,
            "health_status": l.health_status
        }
        for l in livestock_list
    ]
    return jsonify({"livestock": results}), 200


# UPDATE livestock (user can only update livestock of their farms)
# UPDATE livestock (user can only update livestock of their farms)
@livestock_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_livestock(id):
    user_id = get_jwt_identity()
    livestock = Livestock.query.get(id)

    if not livestock:
        return jsonify({"error": "Livestock not found"}), 404

    # Check that the livestock's farm belongs to this user
    farm = Farm.query.filter_by(farm_id=livestock.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Not authorized to update this livestock"}), 403

    data = request.get_json()
    if data:
        livestock.animal_type = data.get("animal_type", livestock.animal_type)
        livestock.quantity = data.get("quantity", livestock.quantity)
        livestock.purchase_date = data.get("purchase_date", livestock.purchase_date)
        livestock.health_status = data.get("health_status", livestock.health_status)

        db.session.commit()

    return jsonify({"message": "Livestock updated successfully"}), 200



# DELETE livestock (user can only delete livestock of their farms)
@livestock_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_livestock(id):
    user_id = get_jwt_identity()
    livestock = Livestock.query.get(id)

    if not livestock:
        return jsonify({"error": "Livestock not found"}), 404

    # Check that the livestock's farm belongs to this user
    farm = Farm.query.filter_by(farm_id=livestock.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Not authorized to delete this livestock"}), 403

    db.session.delete(livestock)
    db.session.commit()
    return jsonify({"message": "Livestock deleted successfully"}), 200
# DELETE livestock (user can only delete livestock of their farms)
# @livestock_bp.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
# def delete_livestock(id):
#     user_id = get_jwt_identity()
#     livestock = Livestock.query.get(id)
#
#     if not livestock:
#         return jsonify({"error": "Livestock not found"}), 404
#
#     # Check that the livestock's farm belongs to this user
#     if livestock.farm.user_id != user_id:
#         return jsonify({"error": "Not authorized to delete this livestock"}), 403
#
#     db.session.delete(livestock)
#     db.session.commit()
#     return jsonify({"message": "Livestock deleted successfully"}), 200