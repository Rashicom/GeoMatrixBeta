from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geomatrix.config import get_settings

settings = get_settings()

# establishing connection to database server
engine = create_engine(
    url=settings.db_url,
    pool_size=settings.pool_size,
    echo=True,  # print SQL queries to console for debugging
)

# session
SessionLocal = sessionmaker(bind= engine)

# Base Class for orm
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print("database connection established")
        yield db
    finally:
        print("connection to database closed")
        db.close()
