from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))

    portfolio = relationship("Portfolio", back_populates="investments")
    transactions = relationship("Transaction", back_populates="investment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Investment(id={self.id}, name='{self.name}', value={self.value})"
