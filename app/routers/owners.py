from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..deps import get_current_user, get_db

router = APIRouter(
    prefix="/owners",
    tags=["Propietarios"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=schemas.OwnerRead, status_code=status.HTTP_201_CREATED)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_owner(db, owner)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un propietario con ese email",
        )


@router.get("/", response_model=List[schemas.OwnerRead])
def list_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_owners(db, skip=skip, limit=limit)


@router.get("/{owner_id}", response_model=schemas.OwnerReadWithPets)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = crud.get_owner(db, owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado"
        )
    return owner


@router.put("/{owner_id}", response_model=schemas.OwnerRead)
def update_owner(
    owner_id: int, owner_update: schemas.OwnerUpdate, db: Session = Depends(get_db)
):
    owner = crud.update_owner(db, owner_id, owner_update)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado"
        )
    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    if not crud.delete_owner(db, owner_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado"
        )
