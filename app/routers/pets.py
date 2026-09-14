from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_current_user, get_db

router = APIRouter(
    prefix="/pets",
    tags=["Mascotas"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=schemas.PetRead, status_code=status.HTTP_201_CREATED)
def create_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    if crud.get_owner(db, pet.owner_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado"
        )
    return crud.create_pet(db, pet)


@router.get("/", response_model=List[schemas.PetRead])
def list_pets(
    owner_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_pets(db, owner_id=owner_id, skip=skip, limit=limit)


@router.get("/{pet_id}", response_model=schemas.PetReadWithAppointments)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = crud.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada"
        )
    return pet


@router.put("/{pet_id}", response_model=schemas.PetRead)
def update_pet(
    pet_id: int, pet_update: schemas.PetUpdate, db: Session = Depends(get_db)
):
    pet = crud.update_pet(db, pet_id, pet_update)
    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada"
        )
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    if not crud.delete_pet(db, pet_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada"
        )
