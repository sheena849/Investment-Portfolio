from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="portfolios", cascade="all, delete-orphan", single_parent=True)
    investments = relationship("Investment", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Portfolio(id={self.id}, name='{self.name}', description='{self.description}', "
            f"budget={self.budget}, company='{self.company.name}')>"
        )
