from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException,status, Response
from sqlalchemy.orm import Session
from .Routers import doctors, patient
from . import crud, database, schemas,models,auth
from .database import get_db, engine
from fastapi.security import OAuth2PasswordRequestForm
from .auth import require_role

import os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(doctors.router)
app.include_router(patient.router)


IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.post("/register", response_model=schemas.UserOut)
def create_user(username: str = Form(...) ,email: str = Form(...),password: str = Form(...),
                role: str = Form("patient"),image: UploadFile = File(None),db: Session = Depends(get_db)):
    
    # Handle file saving 
    image_path = None
    if image:
        image_path = f"app/images/{image.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())

    user_data = schemas.UserCreate(username=username,email=email,password=password,role=role,image=image_path)

    return crud.create_user(user_data, db)


@app.post("/login", response_model=schemas.TokenOut)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:

        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = auth.create_access_token(data={"sub": user.username,"role": user.role })

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.get("/users",response_model=list[schemas.UserOut])
def get_all_users(db:Session=Depends(get_db)):

    all_users=db.query(models.User).all()

    return all_users 

@app.delete("/users/remove/{id}")
def delete_user(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(require_role("admin"))):

    user=db.query(models.User).filter(models.User.id==id).first()

    try : 

        db.delete(user)

        db.commit()

    except:

        db.rollback()

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    