from pydantic import BaseModel

# user schema
class UserBase(BaseModel):
    username: str
    email: str
    
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# flight schema
class FlightBase(BaseModel):
    flight_number: int
    destination: str
    departure: str
    

class Flights(FlightBase):
    id:  int
    user_id: int
    
    class config:
        orm_mode = True
        
class FlightCreate(FlightBase):
    pass
        
class FlightUpdate(FlightBase):
    pass