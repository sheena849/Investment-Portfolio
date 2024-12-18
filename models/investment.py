from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from db_setup import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))  # Link to Company by company_id
    investment_type = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)
    expected_return = Column(String, nullable=False)
    date_invested = Column(Date, nullable=False)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="investments", cascade="all, delete-orphan", single_parent=True)
    company = relationship("Company", back_populates="investments")  # Relationship with Company
    transactions = relationship("Transaction", back_populates="investment", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"Investment(id={self.id}, name='{self.name}', value={self.value}, "
            f"company_name='{self.company.name}', investment_type='{self.investment_type}', "
            f"risk_level='{self.risk_level}', expected_return='{self.expected_return}', "
            f"date_invested='{self.date_invested}')"
        )
