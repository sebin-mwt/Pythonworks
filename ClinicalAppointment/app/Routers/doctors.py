from fastapi import APIRouter, Depends, HTTPException,status
from app import schemas, models, crud
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
router=APIRouter()



@router.post("/slots", response_model=schemas.SlotOut)
def create_slot(slot: schemas.SlotCreate,db: Session = Depends(get_db),current_user: models.User = Depends(require_role("doctor"))):

    return crud.create_slot(slot, current_user, db)


@router.get("/slots",response_model=list[schemas.SlotOut])
def get_all_slots(db:Session=Depends(get_db),current_user:models.User=Depends(require_role("doctor"))):

    return crud.get_slots(db,current_user)


@router.put("/slots/update/{id}", response_model=schemas.SlotOut)
def update_slots(id: int,data: schemas.SlotCreate,db: Session = Depends(get_db),current_user: models.User = Depends(require_role("doctor"))):
    
    slot = db.query(models.AppointmentSlot).filter(models.AppointmentSlot.id == id,models.AppointmentSlot.doctor_id == current_user.id).first()  # Only update own slot

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found or not yours.")
    
    if slot.doctor_id != current_user.id:

        raise HTTPException(status_code=401,detail="Unauthorized to do this task..")

    return crud.update_slot_data(db, slot, data)  

@router.delete("/slots/remove/{id}")
def delete_slot(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(require_role("doctor"))):

    current_slot=db.query(models.AppointmentSlot).filter(models.AppointmentSlot.id==id).first()

    if not current_slot:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Slot not found !!")
    
    if current_user.id != current_slot.doctor_id:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return  crud.delete_slot(db,current_slot)

@router.get("/bookings", response_model=list[schemas.AppointmentOut])
def get_doctors_bookings(db:Session =Depends(get_db), current_user : models.User= Depends(require_role("doctor"))):

    return crud.get_current_doctor_bookings(db,current_user)