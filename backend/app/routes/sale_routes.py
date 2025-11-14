from flask import Blueprint, request, jsonify
from app import db
from app.models.sale import Sale
from app.models.farm import Farm

sale_bp = Blueprint('sales', __name__)

# Get all sales for a farm
@sale_bp.route('/<int:farm_id>/sales', methods=['GET'])
def get_sales(farm_id):
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    sales = Sale.query.filter_by(farm_id=farm_id).all()
    return jsonify([sale.to_dict() for sale in sales]), 200

# Get a single sale
@sale_bp.route('/<int:farm_id>/sales/<int:sale_id>', methods=['GET'])
def get_sale(farm_id, sale_id):
    sale = Sale.query.filter_by(farm_id=farm_id, id=sale_id).first()
    if not sale:
        return jsonify({"error": "Sale not found"}), 404
    return jsonify(sale.to_dict()), 200

# Create a sale
@sale_bp.route('/<int:farm_id>/sales', methods=['POST'])
def create_sale(farm_id):
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    sale = Sale(
        farm_id=farm_id,
        item_name=data.get('item_name'),
        quantity=data.get('quantity'),
        unit_price=data.get('unit_price'),
        total_amount=data.get('quantity') * data.get('unit_price'),
        notes=data.get('notes')
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify(sale.to_dict()), 201

# Update a sale
@sale_bp.route('/<int:farm_id>/sales/<int:sale_id>', methods=['PUT'])
def update_sale(farm_id, sale_id):
    sale = Sale.query.filter_by(farm_id=farm_id, id=sale_id).first()
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    sale.item_name = data.get('item_name', sale.item_name)
    sale.quantity = data.get('quantity', sale.quantity)
    sale.unit_price = data.get('unit_price', sale.unit_price)
    sale.total_amount = sale.quantity * sale.unit_price
    sale.notes = data.get('notes', sale.notes)

    db.session.commit()
    return jsonify(sale.to_dict()), 200

# Delete a sale
@sale_bp.route('/<int:farm_id>/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(farm_id, sale_id):
    sale = Sale.query.filter_by(farm_id=farm_id, id=sale_id).first()
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale deleted"}), 200
