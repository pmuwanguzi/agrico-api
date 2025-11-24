# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import db
# from app.models.sale import Sale
# from app.models.farm import Farm
# from datetime import datetime
#
# # ---------------- Blueprint ----------------
# sales_bp = Blueprint("sales_bp", __name__, url_prefix="/sales")
#
#
# # ---------------- CREATE SALE ----------------
# @sales_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_sales():
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     farm_id = data.get("farm_id")
#     item_name = data.get("item_name")
#     quantity = data.get("quantity")
#     unit_price = data.get("unit_price")
#     total_amount = data.get("total_amount")
#     sale_date = data.get("date")  # optional YYYY-MM-DD
#     notes = data.get("notes")
#     if not farm_id or not quantity:
#         return jsonify({"error": "farm_id and quantity are required"}), 400
#
#     # Ensure the farm belongs to the current user
#     farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
#     if not farm:
#         return jsonify({"error": "Farm not found for this user"}), 404
#
#     sale = Sale(
#         farm_id=farm_id,
#         item_name=item_name,
#         quantity = quantity,
#         unit_price = unit_price,
#         total_amount = quantity * unit_price ,
#         sale_date = datetime.strptime(sale_date, "%Y-%m-%d") if sale_date else datetime.utcnow(),
#         notes = notes
#     )
#     db.session.add(sale)
#     db.session.commit()
#
#     return jsonify({"message": "Sale created", "sale": sale.to_dict()}), 201
#
# #
# # # ---------------- GET ALL SALES FOR A FARM ----------------
# # ---------------- GET ALL SALES FOR A SPECIFIC FARM ----------------
# @sales_bp.route("/farm/<int:farm_id>", methods=["GET"])
# @jwt_required()
# def get_sales_for_farm(farm_id):
#     user_id = get_jwt_identity()
#
#     # 1. Ensure farm belongs to the authenticated user
#     farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
#     if not farm:
#         return jsonify({"error": "Farm not found for this user"}), 404
#
#     # 2. Get all sales for this farm
#     sales = Sale.query.filter_by(farm_id=farm_id).order_by(Sale.sale_date.desc()).all()
#
#     total_amount = sum(sle.total_amount for sle in sales)
#
#     return jsonify({
#         "farm_id": farm_id,
#         "sales_count": len(sales),
#         "total_sales_amount": total_amount,
#         "sales": [sle.to_dict() for sle in sales]
#     }), 200
#
# # @sales_bp.route("/<int:farm_id>", methods=["GET"])
# # @jwt_required()
# # def get_sales(farm_id):
# #     user_id = get_jwt_identity()
# #     # Ensure the farm belongs to the current user
# #     farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
# #     if not farm:
# #         return jsonify({"error": "Farm not found for this user"}), 404
# #
# #     sales = Sale.query.filter_by(farm_id=farm_id).all()
# #     total_amount = sum(sle.total_amount for sle in sales)
# #
# #     return jsonify({
# #         "sales": [sle.to_dict() for sle in sales],
# #         "total_sales": total_amount
# #     }), 200
#
# #
# # # ---------------- UPDATE EXPENSE ----------------
# # @expenses_bp.route("/<int:expense_id>", methods=["PUT"])
# # @jwt_required()
# # def update_expense(expense_id):
# #     user_id = get_jwt_identity()
# #     expense = Expense.query.get(expense_id)
# #     if not expense:
# #         return jsonify({"error": "Expense not found"}), 404
# #
# #     # Ensure the farm of this expense belongs to the user
# #     farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
# #     if not farm:
# #         return jsonify({"error": "You cannot edit expenses for farms that are not yours"}), 403
# #
# #     data = request.get_json()
# #     expense.amount = data.get("amount", expense.amount)
# #     expense.description = data.get("description", expense.description)
# #     date = data.get("date")
# #     if date:
# #         expense.date = datetime.strptime(date, "%Y-%m-%d")
# #
# #     db.session.commit()
# #     return jsonify({"message": "Expense updated", "expense": expense.to_dict()}), 200
# #
# #
# # # ---------------- DELETE EXPENSE ----------------
# # @expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
# # @jwt_required()
# # def delete_expense(expense_id):
# #     user_id = get_jwt_identity()
# #     expense = Expense.query.get(expense_id)
# #     if not expense:
# #         return jsonify({"error": "Expense not found"}), 404
# #
# #     # Ensure the farm of this expense belongs to the user
# #     farm = Farm.query.filter_by(farm_id=expense.farm_id, user_id=user_id).first()
# #     if not farm:
# #         return jsonify({"error": "You cannot delete expenses for farms that are not yours"}), 403
# #
# #     db.session.delete(expense)
# #     db.session.commit()
# #     return jsonify({"message": "Expense deleted"}), 200

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from app import db
from app.models import Sale, Farm

sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


# Helper to get farms for a user
def get_user_farms(user_id):
    return Farm.query.filter_by(user_id=user_id).all()


# CREATE a new sale
@sales_bp.route("/", methods=["POST"])
@jwt_required()
def create_sale():
    user_id = get_jwt_identity()
    data = request.get_json()
    farm_id = data.get("farm_id")

    if not farm_id:
        return jsonify({"error": "farm_id is required"}), 400

    # Check that farm belongs to the user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found or not linked to the user"}), 404

    item_name = data.get("item_name")
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")
    sale_date_str = data.get("sale_date")
    notes = data.get("notes")

    if not item_name or quantity is None or unit_price is None:
        return jsonify({"error": "item_name, quantity, and unit_price are required"}), 400

    try:
        quantity = float(quantity)
        unit_price = float(unit_price)

        if quantity < 0 or unit_price < 0:
            return jsonify({"error": "quantity and unit_price must be non-negative"}), 400

        total_amount = quantity * unit_price

        # Parse sale_date if provided, otherwise use today
        if sale_date_str:
            try:
                sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "sale_date must be in YYYY-MM-DD format"}), 400
        else:
            sale_date = date.today()

        new_sale = Sale(
            farm_id=farm_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            sale_date=sale_date,
            notes=notes
        )

        db.session.add(new_sale)
        db.session.commit()

        return jsonify({
            "message": "Sale created successfully",
            "sale": new_sale.to_dict()
        }), 201

    except ValueError:
        return jsonify({"error": "Invalid number format for quantity or unit_price"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# LIST all sales for user's farms
@sales_bp.route("/", methods=["GET"])
@jwt_required()
def list_sales():
    user_id = get_jwt_identity()
    farms = get_user_farms(user_id)

    if not farms:
        return jsonify({"sales": []}), 200

    farm_ids = [f.farm_id for f in farms]
    sales = Sale.query.filter(Sale.farm_id.in_(farm_ids)).order_by(Sale.sale_date.desc()).all()

    result = [sale.to_dict() for sale in sales]
    return jsonify({"sales": result}), 200


# GET sales for a specific farm
@sales_bp.route("/farm/<int:farm_id>", methods=["GET"])
@jwt_required()
def list_sales_by_farm(farm_id):
    user_id = get_jwt_identity()

    # Check that farm belongs to the user
    farm = Farm.query.filter_by(farm_id=farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Farm not found or not linked to the user"}), 404

    sales = Sale.query.filter_by(farm_id=farm_id).order_by(Sale.sale_date.desc()).all()
    result = [sale.to_dict() for sale in sales]

    return jsonify({"sales": result}), 200


# GET total sales (optionally filtered by date range)
@sales_bp.route("/total", methods=["GET"])
@jwt_required()
def get_total_sales():
    user_id = get_jwt_identity()
    farms = get_user_farms(user_id)

    if not farms:
        return jsonify({"total_sales": 0}), 200

    farm_ids = [f.farm_id for f in farms]

    # Get optional date filters from query params
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    query = Sale.query.filter(Sale.farm_id.in_(farm_ids))

    # Apply date filters if provided
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            query = query.filter(Sale.sale_date >= start_date)
        except ValueError:
            return jsonify({"error": "start_date must be in YYYY-MM-DD format"}), 400

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            query = query.filter(Sale.sale_date <= end_date)
        except ValueError:
            return jsonify({"error": "end_date must be in YYYY-MM-DD format"}), 400

    sales = query.all()
    total = sum(float(sale.total_amount) for sale in sales)

    return jsonify({"total_sales": total}), 200


# UPDATE a sale
@sales_bp.route("/<int:sale_id>", methods=["PUT"])
@jwt_required()
def update_sale(sale_id):
    user_id = get_jwt_identity()
    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    # Check that the sale's farm belongs to this user
    farm = Farm.query.filter_by(farm_id=sale.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Not authorized to update this sale"}), 403

    data = request.get_json()

    try:
        # Update fields if provided
        if "item_name" in data:
            sale.item_name = data["item_name"]

        quantity_updated = False
        price_updated = False

        if "quantity" in data:
            quantity = float(data["quantity"])
            if quantity < 0:
                return jsonify({"error": "quantity must be non-negative"}), 400
            sale.quantity = quantity
            quantity_updated = True

        if "unit_price" in data:
            unit_price = float(data["unit_price"])
            if unit_price < 0:
                return jsonify({"error": "unit_price must be non-negative"}), 400
            sale.unit_price = unit_price
            price_updated = True

        # Recalculate total_amount if quantity or unit_price changed
        if quantity_updated or price_updated:
            sale.total_amount = float(sale.quantity) * float(sale.unit_price)

        if "sale_date" in data:
            try:
                sale.sale_date = datetime.strptime(data["sale_date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "sale_date must be in YYYY-MM-DD format"}), 400

        if "notes" in data:
            sale.notes = data["notes"]

        db.session.commit()
        return jsonify({
            "message": "Sale updated successfully",
            "sale": sale.to_dict()
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE a sale
@sales_bp.route("/<int:sale_id>", methods=["DELETE"])
@jwt_required()
def delete_sale(sale_id):
    user_id = get_jwt_identity()
    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    # Check that the sale's farm belongs to this user
    farm = Farm.query.filter_by(farm_id=sale.farm_id, user_id=user_id).first()
    if not farm:
        return jsonify({"error": "Not authorized to delete this sale"}), 403

    try:
        db.session.delete(sale)
        db.session.commit()
        return jsonify({"message": "Sale deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500