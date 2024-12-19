from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to the User model

    # Relationships
    portfolios = relationship(
        "Portfolio", back_populates="company", cascade="all, delete-orphan", single_parent=True
    )
    investments = relationship(
        "Investment", back_populates="company", cascade="all, delete-orphan", single_parent=True
    )
    transactions = relationship(
        "Transaction", back_populates="company", cascade="all, delete-orphan", single_parent=True
    )
    user = relationship("User", back_populates="companies")  # Back-reference to the User model

    def __repr__(self):
        return f"Company(id={self.id}, name='{self.name}', industry='{self.industry}')"
