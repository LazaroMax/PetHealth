from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Auth / User ----------
class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Owner ----------
class OwnerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class OwnerRead(OwnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class OwnerReadWithPets(OwnerRead):
    pets: List["PetRead"] = []


# ---------- Pet ----------
class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    owner_id: int


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    owner_id: Optional[int] = None


class PetRead(PetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class PetReadWithAppointments(PetRead):
    appointments: List["AppointmentRead"] = []


# ---------- Appointment ----------
class AppointmentBase(BaseModel):
    pet_id: int
    appointment_date: datetime
    reason: str
    diagnosis: Optional[str] = None
    veterinarian: Optional[str] = None
    status: str = "scheduled"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None
    diagnosis: Optional[str] = None
    veterinarian: Optional[str] = None
    status: Optional[str] = None


class AppointmentRead(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


OwnerReadWithPets.model_rebuild()
PetReadWithAppointments.model_rebuild()
