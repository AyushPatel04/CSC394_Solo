from sqlalchemy import Column, Integer, String
from db import Base

class RestaurantDB(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)

