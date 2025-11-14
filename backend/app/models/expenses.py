from app import db
from datetime import datetime

class Expense(db.Model):
    __tablename__ = "expenses"

    expense_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    # Correct foreign key
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.farm_id'), nullable=False)

    farm = db.relationship('Farm', backref=db.backref('expenses', lazy=True))

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "description": self.description,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "farm_id": self.farm_id
        }

    def __repr__(self):
        return f"<Expense {self.description}>"
