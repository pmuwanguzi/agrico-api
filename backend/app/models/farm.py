from app import db
from datetime import datetime

class Farm(db.Model):
    __tablename__ = "farms"

    farm_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    size_acres = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('farms', lazy=True))

    def __repr__(self):
        return f"<Farm {self.farm_name}>"
