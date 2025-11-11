from app import db
from datetime import datetime


class Crop(db.Model):
    __tablename__ = "crops"

    crop_id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.farm_id"), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(50))
    planting_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    expected_yield = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    farm = db.relationship("Farm", backref=db.backref("crops", lazy=True))

    def __repr__(self):
        return f"<Crop {self.crop_name}>"
