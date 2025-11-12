from datetime import datetime
from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.models.sale import Sale
try:
    from app.models.expense import Expense
    HAS_EXPENSE = True
except Exception:
    HAS_EXPENSE = False

summary_bp = Blueprint("summary", __name__, url_prefix="/farms/<int:farm_id>/summary")

def user_has_farm_access(user_id: int, farm_id: int) -> bool:
    ident = get_jwt_identity()
    if ident and ident.get("role") == "admin":
        return True
    from app.models.farm import Farm
    farm = Farm.query.get(farm_id)
    return bool(farm and getattr(farm, "user_id", None) == user_id)

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def daterange_filters(model_date_col, d_from, d_to, q):
    if d_from:
        q = q.filter(model_date_col >= parse_date(d_from))
    if d_to:
        q = q.filter(model_date_col <= parse_date(d_to))
    return q

@summary_bp.route("/profit", methods=["GET"])
@jwt_required()
def profit_total(farm_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    d_from = request.args.get("from")
    d_to = request.args.get("to")

    q = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0)).filter(Sale.farm_id == farm_id)
    q = daterange_filters(Sale.sale_date, d_from, d_to, q)
    total = q.scalar() or Decimal("0")

    return jsonify({
        "farm_id": farm_id,
        "from": d_from,
        "to": d_to,
        "profit_total": float(total)
    }), 200

@summary_bp.route("/loss", methods=["GET"])
@jwt_required()
def loss_total(farm_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    d_from = request.args.get("from")
    d_to = request.args.get("to")

    if HAS_EXPENSE:
        q = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(Expense.farm_id == farm_id)
        q = daterange_filters(Expense.expense_date, d_from, d_to, q)
        total_loss = q.scalar() or 0
    else:
        # Fallback: treat negative sales as losses (rare, but keeps endpoint functional)
        q = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0))\
            .filter(Sale.farm_id == farm_id, Sale.total_amount < 0)
        q = daterange_filters(Sale.sale_date, d_from, d_to, q)
        total_loss = q.scalar() or 0

    return jsonify({
        "farm_id": farm_id,
        "from": d_from,
        "to": d_to,
        "loss_total": float(abs(total_loss))  # as positive number
    }), 200

@summary_bp.route("", methods=["GET"])
@jwt_required()
def summary(farm_id):
    # Combined summary: profit, loss, net
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    d_from = request.args.get("from")
    d_to = request.args.get("to")

    # profit
    qp = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0)).filter(Sale.farm_id == farm_id)
    qp = daterange_filters(Sale.sale_date, d_from, d_to, qp)
    profit_total = qp.scalar() or 0

    # loss
    if HAS_EXPENSE:
        ql = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(Expense.farm_id == farm_id)
        ql = daterange_filters(Expense.expense_date, d_from, d_to, ql)
        loss_total = ql.scalar() or 0
    else:
        ql = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0))\
            .filter(Sale.farm_id == farm_id, Sale.total_amount < 0)
        ql = daterange_filters(Sale.sale_date, d_from, d_to, ql)
        loss_total = abs(ql.scalar() or 0)

    net = float(profit_total) - float(loss_total)

    return jsonify({
        "farm_id": farm_id,
        "from": d_from,
        "to": d_to,
        "profit_total": float(profit_total),
        "loss_total": float(loss_total),
        "net_income": net
    }), 200
