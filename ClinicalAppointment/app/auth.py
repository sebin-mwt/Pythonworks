from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from . import models
from sqlalchemy.orm import Session
from .database import get_db

SECRET_KEY = "d2cba0ed1eb59922c645c46f1a04c00034cd4ed4f1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

# For extracting token from Authorization header
token_dependency = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(token_dependency),db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


def require_role(required_role: str):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Only {required_role}s are allowed.",
            )
        return current_user
    return role_checker