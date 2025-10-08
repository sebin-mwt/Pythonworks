from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from . import models, schemas


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ------------------ User Functions ------------------

def create_user(db: Session, user: schemas.UserCreate):

    hashed_pwd = hash_password(user.password)
    new_user = models.User(username=user.username,email=user.email,password=hashed_pwd)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except IntegrityError :
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")

def get_user_by_username(db: Session, username: str):

    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):

    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user.password):

        return False
    
    return user

#                           Student Functions 

def create_student(db: Session, student: schemas.StudentCreate,user_id:int):
    new_student = models.Student(**student.dict(),user_id=user_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_student_by_id(db: Session, student_id: int):

    # students= db.query(models.Student).filter(models.Student.user_id==user_id)
    # return students.filter(models.Student.id == student_id).first()

    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session,user_id : int,age: int = None,standard: str = None,place: str = None,is_boy: bool = None,skip: int = 0,limit: int = 10):
   
    query = db.query(models.Student).filter(models.Student.user_id==user_id)
    if age is not None: 
        query = query.filter(models.Student.age == age)
    if standard is not None:
        query = query.filter(models.Student.standard == standard)
    if place is not None:
        query = query.filter(models.Student.place == place)
    if is_boy is not None:
        query = query.filter(models.Student.is_boy == is_boy)

    return query.offset(skip).limit(limit).all()

def update_student(db: Session, student: schemas.StudentCreate,student_id: int,user_id:int):

    student_data = get_student_by_id(db, student_id)
    
    if not student_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No data found !!!")
    
    if student_data.user_id !=user_id:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized to do the task")

    for field, value in student.dict().items():
        setattr(student_data, field, value)

    db.commit()
    db.refresh(student_data)
    return student_data

def delete_student(db: Session, student_id: int,user_id:int):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    if student.user_id !=user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "You are not authorised to do the task")
    
    db.delete(student)  
    db.commit() 
    return student

# search_student(db,query,user_id=current_user.id)
def search_student(db:Session, query:str , user_id:int):

    result=db.query(models.Student).filter(models.Student.user_id==user_id,or_
                                           (models.Student.name.ilike(f"%{query}%"),
                                            models.Student.standard.ilike(f"%{query}%"),
                                            models.Student.place.ilike(f"%{query}%")
                                            )
                                           ).all()
    
    return result