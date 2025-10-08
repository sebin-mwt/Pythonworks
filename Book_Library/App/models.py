from sqlalchemy import Integer , Column, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):

    __tablename__="users"

    id = Column(Integer, primary_key=True,autoincrement=True)

    author = Column(String,unique=True)

    books = relationship("Book",back_populates="user",cascade="all, delete")

    role = Column(String, default="user" ) # possible rolls - user, author , admin

class Book(Base):

    __tablename__="books"

    id = Column(Integer, primary_key=True, autoincrement=True)

    book_name = Column(String)

    rating = Column(Integer)

    user_id = Column(Integer,ForeignKey("users.id"))

    book_file = Column(String)

    uploaded_at = Column(DateTime,default=datetime.utcnow())

    user=relationship("User",back_populates="books")

