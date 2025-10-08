from pydantic import BaseModel
from typing import Optional

class Usercreate(BaseModel):

    author: str

class UserOut(Usercreate):

    id: int 

    class Config:

        from_attributes=True

class BookCreate(BaseModel):

    book_name :str

    rating : Optional[int]=None

    user_id :int

class BookOut(BookCreate):

    id : int 

    class Config:

        from_attributes=True

class BookUpdate(BaseModel):

    book_name: Optional[str]=None

    rating :  Optional[int] =None

    user_id : Optional[int] = None
 
