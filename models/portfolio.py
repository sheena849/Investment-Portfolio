from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db_setup import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    budget = Column(Float, nullable=False)

    investments = relationship("Investment", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Portfolio(id={self.id}, name='{self.name}', budget={self.budget})"
