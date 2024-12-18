from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_setup import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)

    # Relationships
    portfolios = relationship("Portfolio", back_populates="company")
    investments = relationship("Investment", back_populates="company")  # No changes here

    def __repr__(self):
        return f"Company(id={self.id}, name='{self.name}', industry='{self.industry}')"
