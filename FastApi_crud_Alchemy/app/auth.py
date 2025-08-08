from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from . import models, schemas 
from sqlalchemy.orm import Session
from . database import get_db

# Secret key for encoding and decoding the JWT token
SECRET_KEY = "d2cba0ed1eb59922c645c46f1a04c00034cd4ed41a00910654eb8605650d18f1"  # Replace with your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token_dependency  = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def credentials_exception():

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)

def get_current_user(token: str = Depends(token_dependency ), db: Session = Depends(get_db)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception()
        
        user = db.query(models.User).filter(models.User.username == username).first()

        if user is None:
            raise credentials_exception()
        
        return user
    
    except JWTError:
        raise credentials_exception()
