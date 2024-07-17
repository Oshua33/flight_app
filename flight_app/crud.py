from fastapi import Depends
from sqlalchemy.orm import Session
import models
import schemas
import auth



# users crud
def create_user(db: Session, username: str, email: str, hashed_password: str):
    db_user = models.User(username=username, email=email,  hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# flight crud
def create_flight( flight: schemas.FlightCreate, db: Session, user_id: schemas.User):
    db_flight = models.Flight(
        **flight.model_dump(),
        user_id=user_id.id
    )
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def get_flights(db: Session, user_id: schemas.User = Depends(auth.get_current_user), skip: int = 0, limit: int = 10):
    return db.query(models.Flight).filter(models.Flight.user_id == user_id.id).offset(skip).limit(limit).all()

def get_flight(db: Session, id: int):
    return db.query(models.Flight).filter(models.Flight.id == id). first()