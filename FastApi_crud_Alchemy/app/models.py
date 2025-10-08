from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship to Student (One-to-Many)
    students = relationship("Student", back_populates="user")

class Student(Base):
    __tablename__ = "studentss"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)   
    age = Column(Integer, nullable=False)
    standard = Column(String, nullable=False)
    place = Column(String, nullable=False)
    is_boy = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Relationship to User (Many-to-One)
    user = relationship("User", back_populates="students")
