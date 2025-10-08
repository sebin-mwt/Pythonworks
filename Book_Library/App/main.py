from fastapi import FastAPI, Depends,HTTPException,status
from sqlalchemy.orm import Session
from .database import get_db,engine
from .models import User,Book,Base
from .schemas import BookOut, UserOut,Usercreate,BookCreate,BookUpdate
from typing import List

Base.metadata.create_all(bind=engine)
app= FastAPI()

@app.post("/user",response_model=UserOut)
def user_creation(user:Usercreate,db:Session=Depends(get_db)):

    try:
        new_user=User(author=user.author)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except:

        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    return new_user

@app.get("/users",response_model=list[UserOut])
def get_all_users(db:Session=Depends(get_db)):

    all_user=db.query(User).all()
    return all_user

@app.get("/books",response_model=list[BookOut])
def get_all_books(db:Session=Depends(get_db)):

    all_books=db.query(Book).all()

    if not all_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No books found")    
    return all_books

@app.post("/books",response_model=BookOut)
def create_book(book:BookCreate,db:Session=Depends(get_db)):

    new_book=Book(**book.model_dump()) # same as **book.dict()
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

    except:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Database addition failed")

    return new_book


@app.put("/book/{id}",response_model=BookOut)
def update_book(id:int,book:BookCreate,db:Session=Depends(get_db)):

    old_book=db.query(Book).filter(Book.id==id).first()

    if not old_book:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for key,value in book.model_dump(exclude_unset=True).items():

        setattr(old_book,key,value)
    
    try :

        db.commit()
        db.refresh(old_book)

    except: 

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Operation Failed..")
    
    return old_book

@app.patch("/book/{id}")
def patch_book(id:int,book:BookUpdate,db:Session=Depends(get_db)):

    old_book=db.query(Book).filter(Book.id==id).first()

    if not old_book:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data not available")
    
    for key,value in book.model_dump(exclude_unset=True).items():

        setattr(old_book,key,value)

    try :

        db.commit()
        db.refresh(old_book)

    except Exception  as e:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
    
    return old_book

@app.delete("/book/{id}",response_model=BookOut)
def delete_book(id:int,db:Session=Depends(get_db)):

    book=db.query(Book).filter(Book.id==id).first()

    if not book:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    try :

        db.delete(book)
        db.commit()

    except Exception as e :

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
    
    return book