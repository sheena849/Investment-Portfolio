import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set the root logger to INFO level
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)  # Suppress SQLAlchemy engine debug logs

# Define the database URL
DATABASE_URL = "sqlite:///investment.db"  # Using SQLite database

# Setup the database engine with echo=False to prevent SQL statement logs
engine = create_engine(DATABASE_URL, echo=False)

# Setup the sessionmaker
Session = sessionmaker(bind=engine)

# Define the base class for declarative models
Base = declarative_base()
