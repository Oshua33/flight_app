from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False )
    hashed_password = Column(String, nullable=False)

    flight = relationship("Flight", back_populates="user")

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    flight_number = Column(Integer, nullable=False)
    destination = Column(String, nullable=False)
    departure = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="flight")


    