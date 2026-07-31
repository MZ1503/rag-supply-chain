from sqlalchemy import Column, Integer, String, Float, Date, Text,DateTime
from sqlalchemy.sql import func
from app.database import Base

#stores SKU product data

class Product(Base):
    __tablename__ = "products"

    id=Column(Integer,primary_key=True)
    brand=Column(String(100), nullable=False)
    category=Column(String(100), nullable=False)
    storage_temp=Column(String, nullable=True)
    article_code=Column(String(100),nullable=False, unique=True)
    forecast_qty=Column(Integer,nullable=True)
    actual_qty=Column(Integer, nullable=False)
    unit_price_aed=Column(Float,nullable=False)
    expiry_date=Column(Date,nullable=True)
    days_to_expiry=Column(Integer,nullable=True)


# stores every query made to the API

class Query(Base):
    __tablename__= "queries"

    id=Column(Integer,primary_key=True) 
    question=Column(Text)
    answer=Column(Text)
    created_at=Column(DateTime,default=func.now())
    tokens_used=Column(Integer)
    user_id=Column(Integer,nullable=True)


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True)
    email=Column(String(255),nullable=False,unique=True)
    hashed_password=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=func.now())

    
