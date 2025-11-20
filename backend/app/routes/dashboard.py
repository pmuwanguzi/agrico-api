from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Farm, Crop, Livestock
from app.models.expenses import Expense
from app import db

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard_summary():
    user_id = get_jwt_identity()

    # Get user farms
    farms = Farm.query.filter_by(user_id=user_id).all()

    if not farms:
        return jsonify({
            "farms": [],
            "total_livestock": 0,
            "total_crops": 0,
            "total_expenses": 0,
            "livestock_breakdown": {},
            "crop_breakdown": {},
            "recent_livestock": [],
            "recent_crops": [],
            "recent_expenses": []
        }), 200

    farm_ids = [f.farm_id for f in farms]

    # LIVESTOCK
    livestock = Livestock.query.filter(Livestock.farm_id.in_(farm_ids)).all()
    total_livestock = sum(l.quantity for l in livestock)

    livestock_breakdown = {}
    for item in livestock:
        livestock_breakdown[item.animal_type] = livestock_breakdown.get(item.animal_type, 0) + item.quantity

    # CROPS
    crops = Crop.query.filter(Crop.farm_id.in_(farm_ids)).all()
    total_crops = len(crops)

    crop_breakdown = {}
    for crop in crops:
        crop_breakdown[crop.crop_type] = crop_breakdown.get(crop.crop_type, 0) + 1

    # EXPENSES
    expenses = Expense.query.filter(Expense.farm_id.in_(farm_ids)).all()
    total_expenses = sum(exp.amount for exp in expenses)

    # RECENT ITEMS
    recent_livestock = sorted(
        livestock,
        key=lambda x: x.purchase_date or "",
        reverse=True
    )[:5]

    recent_crops = sorted(
        crops,
        key=lambda x: x.planting_date or "",
        reverse=True
    )[:5]

    recent_expenses = sorted(
        expenses,
        key=lambda x: x.date or "",
        reverse=True
    )[:5]

    return jsonify({
        "farms": [
            {
                "farm_id": f.farm_id,
                "farm_name": f.farm_name,
                "location": f.location,
                "size_acres": f.size_acres
            } for f in farms
        ],
        "total_livestock": total_livestock,
        "total_crops": total_crops,
        "total_expenses": total_expenses,

        "livestock_breakdown": livestock_breakdown,
        "crop_breakdown": crop_breakdown,

        "recent_livestock": [
            {
                "id": l.id,
                "farm_id": l.farm_id,
                "animal_type": l.animal_type,
                "quantity": l.quantity,
                "purchase_date": l.purchase_date,
                "health_status": l.health_status
            } for l in recent_livestock
        ],

        "recent_crops": [
            {
                "crop_id": c.crop_id,
                "farm_id": c.farm_id,
                "crop_name": c.crop_name,
                "crop_type": c.crop_type,
                "planting_date": c.planting_date,
                "harvest_date": c.harvest_date,
                "expected_yield": c.expected_yield
            } for c in recent_crops
        ],

        "recent_expenses": [
            exp.to_dict() for exp in recent_expenses
        ]
    })
