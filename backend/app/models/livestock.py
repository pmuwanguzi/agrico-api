from app import db
from datetime import datetime

class Livestock(db.Model):
    __tablename__ = "livestock"

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.farm_id"), nullable=False)
    animal_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.Date, default=datetime.utcnow)
    health_status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Livestock {self.animal_type} - {self.quantity}>"