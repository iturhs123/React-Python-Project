from sqlalchemy import String, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price=Column(Float)
    description= Column(String)
    quantity=Column(Integer)

      # we use columns to define the table structure