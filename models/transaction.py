from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # e.g., "buy" or "sell"
    amount = Column(Float, nullable=False)
    investment_id = Column(Integer, ForeignKey("investments.id"))

    investment = relationship("Investment", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, type='{self.type}', amount={self.amount})"
