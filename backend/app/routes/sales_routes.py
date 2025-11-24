# # app/routes/sales_routes.py
#
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime
# from app import db
# from app.models.sale import Sale
# from app.models.farm import Farm
# from app.models.user import User
#
# sales_bp = Blueprint("sales_bp", __name__, url_prefix="/sales")
#
# # ---------------- Helper ----------------
# def get_user_farm(user_id):
#     """Return the farm linked to the user, or None if none exists."""
#     user = User.query.get(user_id)
#     if user and hasattr(user, "farm") and user.farm:
#         return user.farm
#     return None
#
# # ---------------- CREATE SALE ----------------
# @sales_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_sale():
#     user_id = get_jwt_identity()
#     farm = get_user_farm(user_id)
#     if not farm:
#         return jsonify({"error": "You must have a farm to create sales."}), 403
#
#     data = request.get_json()
#     item_name = data.get("item_name")
#     quantity = data.get("quantity")
#     unit_price = data.get("unit_price")
#     notes = data.get("notes")
#     sale_date_str = data.get("sale_date")
#
#     if not item_name or quantity is None or unit_price is None:
#         return jsonify({"error": "item_name, quantity and unit_price are required"}), 400
#
#     try:
#         quantity = float(quantity)
#         unit_price = float(unit_price)
#         total_amount = quantity * unit_price
#         sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d").date() if sale_date_str else datetime.today().date()
#     except ValueError:
#         return jsonify({"error": "Invalid numeric values or date format"}), 400
#
#     sale = Sale(
#         farm_id=farm.farm_id,
#         item_name=item_name,
#         quantity=quantity,
#         unit_price=unit_price,
#         total_amount=total_amount,
#         sale_date=sale_date,
#         notes=notes
#     )
#     db.session.add(sale)
#     db.session.commit()
#
#     return jsonify({"message": "Sale created successfully", "sale": sale.to_dict()}), 201
#
# # ---------------- GET ALL SALES ----------------
# @sales_bp.route("/", methods=["GET"])
# @jwt_required()
# def get_sales():
#     user_id = get_jwt_identity()
#     farm = get_user_farm(user_id)
#     if not farm:
#         return jsonify({"error": "You must have a farm to view sales."}), 403
#
#     sales = Sale.query.filter_by(farm_id=farm.farm_id).order_by(Sale.sale_date.desc()).all()
#     return jsonify([s.to_dict() for s in sales]), 200
#
# # ---------------- UPDATE SALE ----------------
# @sales_bp.route("/<int:sale_id>", methods=["PUT"])
# @jwt_required()
# def update_sale(sale_id):
#     user_id = get_jwt_identity()
#     farm = get_user_farm(user_id)
#     if not farm:
#         return jsonify({"error": "You must have a farm to update sales."}), 403
#
#     sale = Sale.query.get(sale_id)
#     if not sale or sale.farm_id != farm.farm_id:
#         return jsonify({"error": "Sale not found"}), 404
#
#     data = request.get_json()
#     sale.item_name = data.get("item_name", sale.item_name)
#     sale.quantity = float(data.get("quantity", sale.quantity))
#     sale.unit_price = float(data.get("unit_price", sale.unit_price))
#     sale.total_amount = sale.quantity * sale.unit_price
#     if "sale_date" in data:
#         sale.sale_date = datetime.strptime(data["sale_date"], "%Y-%m-%d").date()
#     sale.notes = data.get("notes", sale.notes)
#
#     db.session.commit()
#     return jsonify({"message": "Sale updated successfully", "sale": sale.to_dict()}), 200
#
# # ---------------- DELETE SALE ----------------
# @sales_bp.route("/<int:sale_id>", methods=["DELETE"])
# @jwt_required()
# def delete_sale(sale_id):
#     user_id = get_jwt_identity()
#     farm = get_user_farm(user_id)
#     if not farm:
#         return jsonify({"error": "You must have a farm to delete sales."}), 403
#
#     sale = Sale.query.get(sale_id)
#     if not sale or sale.farm_id != farm.farm_id:
#         return jsonify({"error": "Sale not found"}), 404
#
#     db.session.delete(sale)
#     db.session.commit()
#     return jsonify({"message": "Sale deleted successfully"}), 200
#
# # ---------------- TOTAL SALES FOR PERIOD ----------------
# @sales_bp.route("/total", methods=["GET"])
# @jwt_required()
# def total_sales():
#     user_id = get_jwt_identity()
#     farm = get_user_farm(user_id)
#     if not farm:
#         return jsonify({"error": "You must have a farm to view sales."}), 403
#
#     start_date_str = request.args.get("start_date")
#     end_date_str = request.args.get("end_date")
#     try:
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
#         end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
#     except ValueError:
#         return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
#
#     query = Sale.query.filter_by(farm_id=farm.farm_id)
#     if start_date:
#         query = query.filter(Sale.sale_date >= start_date)
#     if end_date:
#         query = query.filter(Sale.sale_date <= end_date)
#
#     total = sum([s.total_amount for s in query.all()])
#     return jsonify({"total_sales": float(total)}), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.sale import Sale
from app.models.farm import Farm
from datetime import datetime

# ---------------- Blueprint ----------------
sales_bp = Blueprint("sales_bp", __name__, url_prefix="/sales")


# ---------------- CREATE SALE ----------------
@sales_bp.route("/", methods=["POST"])
@jwt_required()
def create_sales():
    user_id = get_jwt_identity()
    data = request.get_json()
    farm_id = data.get("farm_id")
    item_name = data.get("item_name")
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")
    total_amount = data.get("total_amount")
    sale_date = data.get("date")  # optional YYYY-MM-DD
    notes = data.get("notes")
    if not farm_id or not quantity:
        return jsonify({"error": "farm_id and quantity are required"}), 400

    # Ensure the farm belongs to the current user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found for this user"}), 404

    sale = Sale(
        farm_id=farm_id,
        item_name=item_name,
        quantity = quantity,
        unit_price = unit_price,
        total_amount = quantity * unit_price ,
        sale_date = datetime.strptime(sale_date, "%Y-%m-%d") if sale_date else datetime.utcnow(),
        notes = notes
    )
    db.session.add(sale)
    db.session.commit()

    return jsonify({"message": "Sale created", "sale": sale.to_dict()}), 201

#
# # ---------------- GET ALL SALES FOR A FARM ----------------
# ---------------- GET ALL SALES FOR A SPECIFIC FARM ----------------
@sales_bp.route("/farm/<int:farm_id>", methods=["GET"])
@jwt_required()
def get_sales_for_farm(farm_id):
    user_id = get_jwt_identity()

    # 1. Ensure farm belongs to the authenticated user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found for this user"}), 404

    # 2. Get all sales for this farm
    sales = Sale.query.filter_by(farm_id=farm_id).order_by(Sale.sale_date.desc()).all()

    total_amount = sum(sle.total_amount for sle in sales)

    return jsonify({
        "farm_id": farm_id,
        "sales_count": len(sales),
        "total_sales_amount": total_amount,
        "sales": [sle.to_dict() for sle in sales]
    }), 200

# @sales_bp.route("/<int:farm_id>", methods=["GET"])
# @jwt_required()
# def get_sales(farm_id):
#     user_id = get_jwt_identity()
#     # Ensure the farm belongs to the current user
#     farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
#     if not farm:
#         return jsonify({"error": "Farm not found for this user"}), 404
#
#     sales = Sale.query.filter_by(farm_id=farm_id).all()
#     total_amount = sum(sle.total_amount for sle in sales)
#
#     return jsonify({
#         "sales": [sle.to_dict() for sle in sales],
#         "total_sales": total_amount
#     }), 200

#
# # ---------------- UPDATE EXPENSE ----------------
# @expenses_bp.route("/<int:expense_id>", methods=["PUT"])
# @jwt_required()
# def update_expense(expense_id):
#     user_id = get_jwt_identity()
#     expense = Expense.query.get(expense_id)
#     if not expense:
#         return jsonify({"error": "Expense not found"}), 404
#
#     # Ensure the farm of this expense belongs to the user
#     farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
#     if not farm:
#         return jsonify({"error": "You cannot edit expenses for farms that are not yours"}), 403
#
#     data = request.get_json()
#     expense.amount = data.get("amount", expense.amount)
#     expense.description = data.get("description", expense.description)
#     date = data.get("date")
#     if date:
#         expense.date = datetime.strptime(date, "%Y-%m-%d")
#
#     db.session.commit()
#     return jsonify({"message": "Expense updated", "expense": expense.to_dict()}), 200
#
#
# # ---------------- DELETE EXPENSE ----------------
# @expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
# @jwt_required()
# def delete_expense(expense_id):
#     user_id = get_jwt_identity()
#     expense = Expense.query.get(expense_id)
#     if not expense:
#         return jsonify({"error": "Expense not found"}), 404
#
#     # Ensure the farm of this expense belongs to the user
#     farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
#     if not farm:
#         return jsonify({"error": "You cannot delete expenses for farms that are not yours"}), 403
#
#     db.session.delete(expense)
#     db.session.commit()
#     return jsonify({"message": "Expense deleted"}), 200
