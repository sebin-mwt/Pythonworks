from sqlalchemy import String,Integer,Column, Enum, ForeignKey, Time, Date, Boolean
from sqlalchemy.orm import relationship
from . database import Base
from enum import Enum as PyEnum

class Useroption(str, PyEnum):

    admin="admin"
    doctor="doctor"
    patient="patient"

class User(Base):

    __tablename__="userss"

    id= Column(Integer, primary_key=True)
    
    username= Column(String,nullable=False,unique=True)

    email= Column(String,nullable=False, unique=True)

    password= Column(String, nullable=False)

    role = Column(Enum(Useroption),default=Useroption.patient)

    image= Column(String,default=None)

    # Relations
    slots=relationship("AppointmentSlot",back_populates="doctor",cascade="all, delete-orphan")
    
    appointments = relationship("Appointment",back_populates="patient",cascade="all , delete-orphan")

class AppointmentSlot(Base):

    __tablename__="appointmentSlots"

    id = Column(Integer,primary_key=True,nullable=False)

    doctor_id = Column(Integer,ForeignKey("userss.id"),nullable=False)

    start_time=Column(Time,nullable=False)

    end_time= Column(Time,nullable=False)

    date= Column(Date, nullable=False)

    is_available= Column(Boolean,default=True)

    #Relations
    doctor=relationship("User",back_populates="slots")
    appointment = relationship("Appointment",back_populates="slot",uselist=False)

class Appointment(Base):

    __tablename__="appointments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer,ForeignKey("userss.id"),nullable=False)

    slot_id = Column(Integer, ForeignKey("appointmentSlots.id"),nullable=False,unique=True)

    status= Column(String, default="Booked")

    #Relationships

    patient= relationship("User",back_populates="appointments")

    slot= relationship("AppointmentSlot",back_populates="appointment")

