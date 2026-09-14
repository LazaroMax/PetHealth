from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas
from .security import hash_password


# ---------- User ----------
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username, hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- Owner ----------
def create_owner(db: Session, owner: schemas.OwnerCreate) -> models.Owner:
    db_owner = models.Owner(**owner.model_dump())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def get_owner(db: Session, owner_id: int) -> Optional[models.Owner]:
    return db.query(models.Owner).filter(models.Owner.id == owner_id).first()


def get_owners(db: Session, skip: int = 0, limit: int = 100) -> List[models.Owner]:
    return db.query(models.Owner).offset(skip).limit(limit).all()


def update_owner(
    db: Session, owner_id: int, owner_update: schemas.OwnerUpdate
) -> Optional[models.Owner]:
    db_owner = get_owner(db, owner_id)
    if db_owner is None:
        return None
    for field, value in owner_update.model_dump(exclude_unset=True).items():
        setattr(db_owner, field, value)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def delete_owner(db: Session, owner_id: int) -> bool:
    db_owner = get_owner(db, owner_id)
    if db_owner is None:
        return False
    db.delete(db_owner)
    db.commit()
    return True


# ---------- Pet ----------
def create_pet(db: Session, pet: schemas.PetCreate) -> models.Pet:
    db_pet = models.Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def get_pet(db: Session, pet_id: int) -> Optional[models.Pet]:
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()


def get_pets(
    db: Session, owner_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[models.Pet]:
    query = db.query(models.Pet)
    if owner_id is not None:
        query = query.filter(models.Pet.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def update_pet(
    db: Session, pet_id: int, pet_update: schemas.PetUpdate
) -> Optional[models.Pet]:
    db_pet = get_pet(db, pet_id)
    if db_pet is None:
        return None
    for field, value in pet_update.model_dump(exclude_unset=True).items():
        setattr(db_pet, field, value)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def delete_pet(db: Session, pet_id: int) -> bool:
    db_pet = get_pet(db, pet_id)
    if db_pet is None:
        return False
    db.delete(db_pet)
    db.commit()
    return True


# ---------- Appointment ----------
def create_appointment(
    db: Session, appointment: schemas.AppointmentCreate
) -> models.Appointment:
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )


def get_appointments(
    db: Session, pet_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[models.Appointment]:
    query = db.query(models.Appointment)
    if pet_id is not None:
        query = query.filter(models.Appointment.pet_id == pet_id)
    return query.offset(skip).limit(limit).all()


def update_appointment(
    db: Session, appointment_id: int, appointment_update: schemas.AppointmentUpdate
) -> Optional[models.Appointment]:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment is None:
        return None
    for field, value in appointment_update.model_dump(exclude_unset=True).items():
        setattr(db_appointment, field, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment is None:
        return False
    db.delete(db_appointment)
    db.commit()
    return True
