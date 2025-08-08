from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_ ,String,Cast
from ..auth import require_role
from . .database import get_db
from .. import crud, models, schemas
from ..core.email_utils import send_email_apis
router=APIRouter()

@router.post("/appointments",response_model=dict)
async def book_appointments(data:schemas.AppointmentCreate, db:Session=Depends(get_db), current_user:models.User=Depends(require_role("patient"))):


    appoints= crud.create_appointment(db,user_id=current_user.id, slot_id=data.slot_id)

    if appoints:

        await send_email_apis(to_mail=current_user.email,username=current_user.username)

        return {

                "Message":schemas.AppointmentOut.from_orm(appoints),
                "Mess":"Mail sended successfully"
                    
                }
    


    raise HTTPException(status_code=404)

@router.get("/slots/available",response_model=list[schemas.SlotOut])
def available_slots(db:Session=Depends(get_db)):

    return crud.available_slots(db)


@router.get("/my-appointment", response_model=list[schemas.AppointmentOut])
def user_bookings(db:Session=Depends(get_db), current_user:models.User=Depends(require_role("patient"))):
    
    return crud.get_mybookings(db,current_user)


@router.get("/doctor/search/")
def search_doctor(query:str, db:Session=Depends(get_db)):

    data =db.query(models.User).join(models.AppointmentSlot, models.AppointmentSlot.doctor_id == models.User.id).filter(
            models.User.role == "doctor",
            or_(
                models.User.username.ilike(f"%{query}%"),
                Cast(models.AppointmentSlot.start_time,String).ilike(f"%{query}%")
            )).all()
    
    if not data:
        raise HTTPException(status_code=404, detail="No matching doctors found.")

    return data