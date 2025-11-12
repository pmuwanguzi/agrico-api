from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from app import db
from app.models.sale import Sale
from app.models.farm import Farm
# from app.models.user import User  # if you need to check roles

sale_bp = Blueprint("sales", __name__, url_prefix="/farms/<int:farm_id>/sales")

# --- helpers ---
def user_has_farm_access(user_id: int, farm_id: int) -> bool:
    # Admins can be checked from your user model/role; here we assume request has role in identity
    # Replace with your actual check (farm_membership table, etc.)
    ident = get_jwt_identity()  # e.g., {"user_id": 1, "role": "admin"}
    if ident and ident.get("role") == "admin":
        return True
    # Non-admins: ensure farm exists and (optionally) belongs to this user
    farm = Farm.query.get(farm_id)
    if not farm:
        return False
    # If Farm has user_id owner:
    return getattr(farm, "user_id", None) == user_id

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

# --- endpoints ---

@sale_bp.route("", methods=["GET"])
@jwt_required()
def list_sales(farm_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    q = Sale.query.filter_by(farm_id=farm_id)

    # Optional filters: ?from=YYYY-MM-DD&to=YYYY-MM-DD
    d_from = request.args.get("from")
    d_to = request.args.get("to")
    if d_from:
        q = q.filter(Sale.sale_date >= parse_date(d_from))
    if d_to:
        q = q.filter(Sale.sale_date <= parse_date(d_to))

    # Basic pagination
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("pageSize", 20)), 100)
    items = q.order_by(Sale.sale_date.desc(), Sale.id.desc()).paginate(page=page, per_page=page_size, error_out=False)

    return jsonify({
        "data": [s.to_dict() for s in items.items],
        "page": page,
        "pageSize": page_size,
        "total": items.total
    }), 200


@sale_bp.route("", methods=["POST"])
@jwt_required()
def create_sale(farm_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    body = request.get_json() or {}
    required = ["item_name", "quantity", "unit_price"]
    missing = [f for f in required if body.get(f) is None]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    try:
        quantity = float(body["quantity"])
        unit_price = float(body["unit_price"])
        total_amount = quantity * unit_price
    except Exception:
        return jsonify({"error": "quantity/unit_price must be numbers"}), 400

    sale = Sale(
        farm_id=farm_id,
        item_name=body["item_name"],
        quantity=quantity,
        unit_price=unit_price,
        total_amount=total_amount,
        sale_date=parse_date(body["sale_date"]) if body.get("sale_date") else None,
        notes=body.get("notes")
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify(sale.to_dict()), 201


@sale_bp.route("/<int:sale_id>", methods=["PATCH"])
@jwt_required()
def update_sale(farm_id, sale_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    sale = Sale.query.filter_by(id=sale_id, farm_id=farm_id).first()
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    body = request.get_json() or {}
    if "item_name" in body:
        sale.item_name = body["item_name"]
    if "quantity" in body:
        sale.quantity = float(body["quantity"])
    if "unit_price" in body:
        sale.unit_price = float(body["unit_price"])
    if "sale_date" in body:
        sale.sale_date = parse_date(body["sale_date"])
    if "notes" in body:
        sale.notes = body["notes"]

    # keep total_amount consistent
    sale.total_amount = float(sale.quantity) * float(sale.unit_price)

    db.session.commit()
    return jsonify(sale.to_dict()), 200


@sale_bp.route("/<int:sale_id>", methods=["DELETE"])
@jwt_required()
def delete_sale(farm_id, sale_id):
    ident = get_jwt_identity()
    if not user_has_farm_access(ident["user_id"], farm_id):
        return jsonify({"error": "Forbidden"}), 403

    sale = Sale.query.filter_by(id=sale_id, farm_id=farm_id).first()
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    db.session.delete(sale)
    db.session.commit()
    return "", 204
