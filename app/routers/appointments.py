from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_current_user, get_db

router = APIRouter(
    prefix="/appointments",
    tags=["Citas médicas"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/", response_model=schemas.AppointmentRead, status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    if crud.get_pet(db, appointment.pet_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada"
        )
    return crud.create_appointment(db, appointment)


@router.get("/", response_model=List[schemas.AppointmentRead])
def list_appointments(
    pet_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_appointments(db, pet_id=pet_id, skip=skip, limit=limit)


@router.get("/{appointment_id}", response_model=schemas.AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db, appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return appointment


@router.put("/{appointment_id}", response_model=schemas.AppointmentRead)
def update_appointment(
    appointment_id: int,
    appointment_update: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
):
    appointment = crud.update_appointment(db, appointment_id, appointment_update)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    if not crud.delete_appointment(db, appointment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
