from pydantic import BaseModel

class UserCreate(BaseModel):

    email : str

    username: str

    password: str

class UserOut(BaseModel):

    id : int

    email : str

    username : str

    class Config:   

        from_attributes=True

class StudentCreate(BaseModel):

    name : str
    age : int
    standard : str
    place : str
    is_boy : bool =False
    
class StudentOut(StudentCreate):

    id : int
    user_id : int
    class Config :

        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str
