from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from passlib.context import CryptContext

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash plain password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password during login
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Authenticate user during login
def authenticate_user(db: Session, username: str, password: str):

    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    
    return user

# Create new user
def create_user(user: schemas.UserCreate, db: Session):

    hashed_password = hash_password(user.password)
    user_data = user.dict(exclude={"password"})

    new_user = models.User(**user_data, password=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists!")

def create_slot(slot_data: schemas.SlotCreate, current_user: models.User, db: Session):

    if current_user.role != "doctor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only doctors can create slots")

    new_slot = models.AppointmentSlot(doctor_id=current_user.id, start_time=slot_data.start_time,end_time=slot_data.end_time,date=slot_data.date)

    db.add(new_slot) 
    db.commit()
    db.refresh(new_slot)
    return new_slot

def create_appointment(db: Session, user_id: int, slot_id: int):

    # Check if slot exists
    slot = db.query(models.AppointmentSlot).filter(models.AppointmentSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if not slot.is_available:
        raise HTTPException(status_code=400, detail="Slot is already booked")

    # Create appointment
    appointment = models.Appointment(user_id=user_id, slot_id=slot_id)
    db.add(appointment)

    # Mark slot as unavailable
    slot.is_available = False
    db.commit()
    db.refresh(appointment)

    return appointment

def available_slots(db:Session):

    return db.query(models.AppointmentSlot).filter(models.AppointmentSlot.is_available==True).all()

def get_current_doctor_bookings(db: Session, current_user: models.User):

    bookings = db.query(models.Appointment).join(models.Appointment.slot).filter(models.AppointmentSlot.doctor_id == current_user.id).all()

    return bookings 

def get_mybookings(db:  Session, current_user:models.User):

    bookings = db.query(models.Appointment).join(models.Appointment.slot).filter(models.Appointment.user_id == current_user.id, models.AppointmentSlot.is_available==False).all()
    
    return bookings

def get_slots(db:Session,current_user:models.User):

    all_slots=db.query(models.AppointmentSlot).filter(models.AppointmentSlot.doctor_id==current_user.id)

    return all_slots

def update_slot_data(db: Session, slot: models.AppointmentSlot, data: schemas.SlotCreate):

    try:
        slot.date = data.date
        slot.start_time = data.start_time
        slot.end_time = data.end_time

        db.commit()
        db.refresh(slot)
        return slot
    
    except:
        
        db.rollback()
        raise HTTPException(status_code=400, detail="Slot update failed")
    
def delete_slot(db:Session,slot:models.AppointmentSlot):

    try :

        db.delete(slot)
        db.commit()


    except :

        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Deletion Failed !!")