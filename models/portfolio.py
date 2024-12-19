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
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Add this line for the foreign key to User

    # Relationships
    company = relationship("Company", back_populates="portfolios", single_parent=True)
    investments = relationship("Investment", back_populates="portfolio", single_parent=True)
    transactions = relationship("Transaction", back_populates="portfolio", single_parent=True)
    user = relationship("User", back_populates="portfolios")  # Add relationship to User

    def __repr__(self):
        return (
            f"<Portfolio(id={self.id}, name='{self.name}', description='{self.description}', "
            f"budget={self.budget}, company='{self.company.name}')>"
        )
