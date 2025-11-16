from datetime import date
from sqlalchemy import CheckConstraint, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app import db

class Sale(db.Model):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # sale_id
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.farm_id", ondelete="CASCADE"), nullable=False)

    item_name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)  # quantity * unit_price
    sale_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    notes: Mapped[str | None]

    farm = relationship("Farm", backref="sales", lazy="joined")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_sales_quantity_nonneg"),
        CheckConstraint("unit_price >= 0", name="ck_sales_unit_price_nonneg"),
    )

    def to_dict(self):
        return {
            "sale_id": self.id,
            "farm_id": self.farm_id,
            "item_name": self.item_name,
            "quantity": float(self.quantity),
            "unit_price": float(self.unit_price),
            "total_amount": float(self.total_amount),
            "sale_date": self.sale_date.isoformat(),
            "notes": self.notes
        }
