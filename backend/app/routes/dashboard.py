# from flask import Blueprint, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.models import Farm, Crop, Livestock
# from app.models.expenses import Expense
# from app import db
#
# dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")
#
#
# @dashboard_bp.route("/", methods=["GET"])
# @jwt_required()
# def dashboard_summary():
#     user_id = get_jwt_identity()
#
#     # Get user farms
#     farms = Farm.query.filter_by(user_id=user_id).all()
#
#     if not farms:
#         return jsonify({
#             "farms": [],
#             "total_livestock": 0,
#             "total_crops": 0,
#             "total_expenses": 0,
#             "livestock_breakdown": {},
#             "crop_breakdown": {},
#             "recent_livestock": [],
#             "recent_crops": [],
#             "recent_expenses": []
#         }), 200
#
#     farm_ids = [f.farm_id for f in farms]
#
#     # LIVESTOCK
#     livestock = Livestock.query.filter(Livestock.farm_id.in_(farm_ids)).all()
#     total_livestock = sum(l.quantity for l in livestock)
#
#     livestock_breakdown = {}
#     for item in livestock:
#         livestock_breakdown[item.animal_type] = livestock_breakdown.get(item.animal_type, 0) + item.quantity
#
#     # CROPS
#     crops = Crop.query.filter(Crop.farm_id.in_(farm_ids)).all()
#     total_crops = len(crops)
#
#     crop_breakdown = {}
#     for crop in crops:
#         crop_breakdown[crop.crop_type] = crop_breakdown.get(crop.crop_type, 0) + 1
#
#     # EXPENSES
#     expenses = Expense.query.filter(Expense.farm_id.in_(farm_ids)).all()
#     total_expenses = sum(exp.amount for exp in expenses)
#
#     # RECENT ITEMS
#     recent_livestock = sorted(
#         livestock,
#         key=lambda x: x.purchase_date or "",
#         reverse=True
#     )[:5]
#
#     recent_crops = sorted(
#         crops,
#         key=lambda x: x.planting_date or "",
#         reverse=True
#     )[:5]
#
#     recent_expenses = sorted(
#         expenses,
#         key=lambda x: x.date or "",
#         reverse=True
#     )[:5]
#
#     return jsonify({
#         "farms": [
#             {
#                 "farm_id": f.farm_id,
#                 "farm_name": f.farm_name,
#                 "location": f.location,
#                 "size_acres": f.size_acres
#             } for f in farms
#         ],
#         "total_livestock": total_livestock,
#         "total_crops": total_crops,
#         "total_expenses": total_expenses,
#
#         "livestock_breakdown": livestock_breakdown,
#         "crop_breakdown": crop_breakdown,
#
#         "recent_livestock": [
#             {
#                 "id": l.id,
#                 "farm_id": l.farm_id,
#                 "animal_type": l.animal_type,
#                 "quantity": l.quantity,
#                 "purchase_date": l.purchase_date,
#                 "health_status": l.health_status
#             } for l in recent_livestock
#         ],
#
#         "recent_crops": [
#             {
#                 "crop_id": c.crop_id,
#                 "farm_id": c.farm_id,
#                 "crop_name": c.crop_name,
#                 "crop_type": c.crop_type,
#                 "planting_date": c.planting_date,
#                 "harvest_date": c.harvest_date,
#                 "expected_yield": c.expected_yield
#             } for c in recent_crops
#         ],
#
#         "recent_expenses": [
#             exp.to_dict() for exp in recent_expenses
#         ]
#     })
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.models import Farm, Livestock, Crop, Sale, Expense

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    """
    Get comprehensive dashboard statistics for the logged-in user.
    Returns totals for livestock, crops, sales, and expenses across all user's farms.
    """
    user_id = get_jwt_identity()

    try:
        # Get all farm IDs for the user
        user_farms = Farm.query.filter_by(user_id=user_id).all()

        if not user_farms:
            return jsonify({
                "total_farms": 0,
                "total_livestock": 0,
                "total_crops": 0,
                "total_sales": 0.0,
                "total_expenses": 0.0,
                "net_profit": 0.0,
                "farms": [],
                "recent_sales": [],
                "recent_expenses": []
            }), 200

        farm_ids = [f.farm_id for f in user_farms]

        # Count total livestock across all farms
        total_livestock = db.session.query(
            func.sum(Livestock.quantity)
        ).filter(
            Livestock.farm_id.in_(farm_ids)
        ).scalar() or 0

        # Count total crop types across all farms
        total_crops = db.session.query(
            func.count(Crop.crop_id)
        ).filter(
            Crop.farm_id.in_(farm_ids)
        ).scalar() or 0

        # Calculate total sales across all farms
        total_sales = db.session.query(
            func.sum(Sale.total_amount)
        ).filter(
            Sale.farm_id.in_(farm_ids)
        ).scalar() or 0.0

        # Calculate total expenses across all farms
        total_expenses = db.session.query(
            func.sum(Expense.amount)
        ).filter(
            Expense.farm_id.in_(farm_ids)
        ).scalar() or 0.0

        # Calculate net profit
        net_profit = float(total_sales) - float(total_expenses)

        # Get recent sales (last 5)
        recent_sales = Sale.query.filter(
            Sale.farm_id.in_(farm_ids)
        ).order_by(
            Sale.sale_date.desc()
        ).limit(5).all()

        # Get recent expenses (last 5)
        recent_expenses = Expense.query.filter(
            Expense.farm_id.in_(farm_ids)
        ).order_by(
            Expense.date.desc()
        ).limit(5).all()

        # Get farm summaries
        farms_summary = []
        for farm in user_farms:
            farm_livestock = db.session.query(
                func.sum(Livestock.quantity)
            ).filter_by(farm_id=farm.farm_id).scalar() or 0

            farm_crops = db.session.query(
                func.count(Crop.crop_id)
            ).filter_by(farm_id=farm.farm_id).scalar() or 0

            farm_sales = db.session.query(
                func.sum(Sale.total_amount)
            ).filter_by(farm_id=farm.farm_id).scalar() or 0.0

            farm_expenses = db.session.query(
                func.sum(Expense.amount)
            ).filter_by(farm_id=farm.farm_id).scalar() or 0.0

            farms_summary.append({
                "farm_id": farm.farm_id,
                "farm_name": farm.farm_name,
                "location": farm.location,
                "size_acres": farm.size_acres,
                "livestock_count": int(farm_livestock),
                "crops_count": int(farm_crops),
                "total_sales": float(farm_sales),
                "total_expenses": float(farm_expenses),
                "profit": float(farm_sales) - float(farm_expenses)
            })

        # Build response
        response = {
            "total_farms": len(user_farms),
            "total_livestock": int(total_livestock),
            "total_crops": int(total_crops),
            "total_sales": float(total_sales),
            "total_expenses": float(total_expenses),
            "net_profit": net_profit,
            "farms": farms_summary,
            "recent_sales": [sale.to_dict() for sale in recent_sales],
            "recent_expenses": [
                {
                    "expense_id": exp.expense_id,
                    "farm_id": exp.farm_id,
                    "amount": float(exp.amount),
                    "description": exp.description,
                    "date": exp.date.isoformat() if exp.date else None
                }
                for exp in recent_expenses
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return jsonify({"error": "Failed to fetch dashboard data"}), 500


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_quick_summary():
    """
    Get a lightweight summary for quick dashboard updates.
    Returns only the key metrics without detailed breakdowns.
    """
    user_id = get_jwt_identity()

    try:
        # Get all farm IDs for the user
        farm_ids = [f.farm_id for f in Farm.query.filter_by(user_id=user_id).all()]

        if not farm_ids:
            return jsonify({
                "total_livestock": 0,
                "total_crops": 0,
                "total_sales": 0.0,
                "total_expenses": 0.0
            }), 200

        # Quick aggregated queries
        total_livestock = db.session.query(
            func.sum(Livestock.quantity)
        ).filter(Livestock.farm_id.in_(farm_ids)).scalar() or 0

        total_crops = db.session.query(
            func.count(Crop.crop_id)
        ).filter(Crop.farm_id.in_(farm_ids)).scalar() or 0

        total_sales = db.session.query(
            func.sum(Sale.total_amount)
        ).filter(Sale.farm_id.in_(farm_ids)).scalar() or 0.0

        total_expenses = db.session.query(
            func.sum(Expense.amount)
        ).filter(Expense.farm_id.in_(farm_ids)).scalar() or 0.0

        return jsonify({
            "total_livestock": int(total_livestock),
            "total_crops": int(total_crops),
            "total_sales": float(total_sales),
            "total_expenses": float(total_expenses),
            "net_profit": float(total_sales) - float(total_expenses)
        }), 200

    except Exception as e:
        print(f"Dashboard summary error: {str(e)}")
        return jsonify({"error": "Failed to fetch summary"}), 500