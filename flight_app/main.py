from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_user
import crud, schemas
from database import engine, Base, get_db
from auth import pwd_context
from typing import Optional



Base.metadata.create_all(bind=engine)

app = FastAPI()

# user auth 
@app.post('/signup', response_model=schemas.User)
def signup(user: schemas.UserCreate, db:Session = Depends(get_db)):
    new_db_user = crud.get_user_by_username(db, username=user.username)
    db_email = crud.get_user_by_email(db, email=user.email)
    hashed_password = pwd_context.hash(user.password)
    if new_db_user or db_email: 
        raise HTTPException(status_code=400, detail="User already exist")
    return crud.create_user(db=db, username=user.username, email=user.email, hashed_password=hashed_password)

# login endpoint
@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# flight api
@app.post('/flights')
def create_flight(payload: schemas.FlightCreate, db: Session = Depends(get_db),  user: schemas.User = Depends(get_current_user)):
    new_flight = crud.create_flight(
        payload,
        db,
        user
    )
    return {'message': 'success', 'data': new_flight}


@app.get("/flights", status_code=200,  response_model= list[schemas.Flights])
def get_flights(skip: int = 0, limit: int = 10,  db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    flights = crud.get_flights(
        skip=skip, 
        limit=limit,
        db = db,   
        user_id = current_user  
    )
    return {'message': 'success', 'data': flights}


@app.get('/flights/{flight_id}', response_model=schemas.Flights)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = crud.get_flight(db, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight
