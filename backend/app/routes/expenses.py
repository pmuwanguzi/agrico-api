from flask import Blueprint, request, jsonify
from app import db
from app.models.expenses import Expense


expenses_bp = Blueprint('expenses', __name__)

# Create a new expense
@expenses_bp.route('', methods=['POST'])
def create_expense():
    data = request.get_json()
    farm_id = data.get('farm_id')
    expense_type = data.get('expense_type')
    amount = data.get('amount')
    description = data.get('description')

    if not farm_id or not expense_type or not amount:
        return jsonify({"error": "farm_id, expense_type, and amount are required"}), 400

    new_expense = Expense(
        farm_id=farm_id,
        expense_type=expense_type,
        amount=amount,
        description=description
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({"message": "Expense created successfully", "expense": {
        "id": new_expense.id,
        "farm_id": new_expense.farm_id,
        "expense_type": new_expense.expense_type,
        "amount": new_expense.amount,
        "description": new_expense.description,
        "date": new_expense.date
    }}), 201


# Get all expenses for a specific farm
@expenses_bp.route('/<int:farm_id>', methods=['GET'])
def get_expenses(farm_id):
    expenses = Expense.query.filter_by(farm_id=farm_id).all()
    results = [{
        "id": exp.id,
        "expense_type": exp.expense_type,
        "amount": exp.amount,
        "description": exp.description,
        "date": exp.date
    } for exp in expenses]

    return jsonify(results), 200


# Update an expense
@expenses_bp.route('/<int:farm_id>/<int:expense_id>', methods=['PUT'])
def update_expense(farm_id, expense_id):
    expense = Expense.query.filter_by(id=expense_id, farm_id=farm_id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json()
    expense.expense_type = data.get('expense_type', expense.expense_type)
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)

    db.session.commit()

    return jsonify({"message": "Expense updated successfully"}), 200


# Delete an expense
@expenses_bp.route('/<int:farm_id>/<int:expense_id>', methods=['DELETE'])
def delete_expense(farm_id, expense_id):
    expense = Expense.query.filter_by(id=expense_id, farm_id=farm_id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted successfully"}), 200
