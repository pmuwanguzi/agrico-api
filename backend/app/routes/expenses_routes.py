from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.expenses import Expense
from app.models.farm import Farm
from datetime import datetime

# ---------------- Blueprint ----------------
expenses_bp = Blueprint("expenses_bp", __name__, url_prefix="/expenses")


# ---------------- CREATE EXPENSE ----------------
@expenses_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json()
    farm_id = data.get("farm_id")
    amount = data.get("amount")
    description = data.get("description")
    date = data.get("date")  # optional YYYY-MM-DD

    if not farm_id or not amount:
        return jsonify({"error": "farm_id and amount are required"}), 400

    # Ensure the farm belongs to the current user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found for this user"}), 404

    expense = Expense(
        farm_id=farm_id,
        amount=amount,
        description=description,
        date=datetime.strptime(date, "%Y-%m-%d") if date else datetime.utcnow()
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense created", "expense": expense.to_dict()}), 201


# ---------------- GET ALL EXPENSES FOR A FARM ----------------
@expenses_bp.route("/<int:farm_id>", methods=["GET"])
@jwt_required()
def get_expenses(farm_id):
    user_id = get_jwt_identity()
    # Ensure the farm belongs to the current user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found for this user"}), 404

    expenses = Expense.query.filter_by(farm_id=farm_id).all()
    total_amount = sum(exp.amount for exp in expenses)

    return jsonify({
        "expenses": [exp.to_dict() for exp in expenses],
        "total_expenses": total_amount
    }), 200


# ---------------- UPDATE EXPENSE ----------------
@expenses_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    # Ensure the farm of this expense belongs to the user
    farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "You cannot edit expenses for farms that are not yours"}), 403

    data = request.get_json()
    expense.amount = data.get("amount", expense.amount)
    expense.description = data.get("description", expense.description)
    date = data.get("date")
    if date:
        expense.date = datetime.strptime(date, "%Y-%m-%d")

    db.session.commit()
    return jsonify({"message": "Expense updated", "expense": expense.to_dict()}), 200


# ---------------- DELETE EXPENSE ----------------
@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    # Ensure the farm of this expense belongs to the user
    farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "You cannot delete expenses for farms that are not yours"}), 403

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"}), 200
