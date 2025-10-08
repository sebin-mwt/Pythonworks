from fastapi import FastAPI,Depends,HTTPException,status
from . import models , schemas, crud, auth
from .database import engine,get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register",response_model=schemas.UserOut)
def register_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

    return crud.create_user(db,user)

@app.post("/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = crud.authenticate_user(db, form_data.username, form_data.password)

    # If user is not found or password is incorrect, raise an error
    if not user:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Create JWT token (access token)
    access_token = auth.create_access_token(data={"sub": user.username})  # `sub` is the username field

    return {"access_token": access_token, "token_type": "bearer"} 

@app.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate,db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)) :
    # print(current_user)
    # The current_user will be automatically populated from the JWT token
    return crud.create_student(db=db, student=student, user_id=current_user.id)

@app.get("/students", response_model=list[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user),  #  Secure route
    age: int = None,standard: str = None,place: str = None,is_boy: bool = None,skip: int = 0,limit: int = 10):

    return crud.get_students(db=db,user_id=current_user.id,age=age,standard=standard,place=place,is_boy=is_boy,skip=skip,limit=limit)

@app.get("/student/search")
def search_student(query:str , db:Session= Depends(get_db),current_user:models.User=Depends(auth.get_current_user)):
    
    searched_data= crud.search_student(db,query,user_id=current_user.id)

    if not searched_data:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data doesnt match")
    
    return searched_data


@app.get("/student/{id}", response_model=schemas.StudentOut)
def get_student_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):

    student = crud.get_student_by_id(db, student_id=id)

    if not student:

        raise HTTPException(status_code=404, detail="Student not found")

    if student.user_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= " Not authorized to do the task !!")

    return student

@app.put("/student/{id}", response_model=schemas.StudentOut)
def update_student(id: int, student: schemas.StudentCreate, db: Session = Depends(get_db) ,current_user: models.User = Depends(auth.get_current_user)):

    db_student = crud.update_student(db=db, student=student, student_id=id,user_id=current_user.id)

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return db_student

@app.delete("/student/{id}", response_model=schemas.StudentOut)
def delete_student(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)):

    db_student = crud.delete_student(db=db, student_id=id,user_id=current_user.id)

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return db_student 