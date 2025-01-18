from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RecipeCost(Base):
    __tablename__ = "recipes_cost"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    list = Column(String(255), nullable=False)
    weight = Column(Integer, nullable=True)
    unit_pkg = Column(String(50), nullable=False)
    price = Column(Float, nullable=True)
    quantity = Column(String(255), nullable=False)
    cost = Column(Float, nullable=True)