from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DevelopmentConfig


engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine)