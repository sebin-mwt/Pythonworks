from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import time, date

class UserCreate(BaseModel):

    username : str

    email : EmailStr

    password : str

    image : Optional [str]= None

    role : Optional[str] = "patient"

class UserOut(BaseModel):

    id :int

    username : str

    email : EmailStr

    role : str

    class Config:

        from_attributes=True


class TokenOut(BaseModel):

    access_token : str

    token_type : str

class SlotCreate(BaseModel):
    
    start_time: time

    end_time: time

    date: date

class SlotOut(SlotCreate):

    id: int
    
    doctor_id: int 

    is_available: bool

    class Config:

        from_attributes = True

class AppointmentCreate(BaseModel):

    slot_id: int

class AppointmentOut(BaseModel):

    id: int

    slot_id: int

    patient : UserOut

    status: str

    class Config:
        
        from_attributes = True