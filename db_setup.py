import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Suppress SQLAlchemy logs (only show warnings/errors)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Set up the database
DATABASE_URL = "sqlite:///investment_portfolio.db"

engine = create_engine(DATABASE_URL, echo=False)  # Turn 'echo' off for cleaner output
Session = sessionmaker(bind=engine)
Base = declarative_base()

