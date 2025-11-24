# from app import db
# from datetime import datetime

# class Livestock(db.Model):
#     __tablename__ = "livestock"
#
#     id = db.Column(db.Integer, primary_key=True)
#     farm_id = db.Column(db.Integer, db.ForeignKey("farms.farm_id"), nullable=False)
#     animal_type = db.Column(db.String(100), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     purchase_date = db.Column(db.Date, default=datetime.utcnow)
#     health_status = db.Column(db.String(100), nullable=True)
#
#     def __repr__(self):
#         return f"<Livestock {self.animal_type} - {self.quantity}>"
#
#
#     class Livestock(db.Model):
#         __tablename__ = 'livestock'
from app import db

class Livestock(db.Model):
    __tablename__ = 'livestock'

    # PRIMARY KEY - This is required!
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key to farms table
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.farm_id'), nullable=False)

    # Livestock details
    animal_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.String(50))
    health_status = db.Column(db.String(100))

    # Relationship to Farm (this allows livestock.farm.user_id)
    farm = db.relationship('Farm', backref='livestock_items')

    def __repr__(self):
        return f'<Livestock {self.animal_type} - Qty: {self.quantity}>'