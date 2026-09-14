from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """Usuario del sistema (veterinario/administrador) usado para autenticación."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Owner(Base):
    """Propietario (dueño de una o más mascotas)."""

    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    """Mascota (paciente) asociada a un propietario."""

    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("Owner", back_populates="pets")
    appointments = relationship(
        "Appointment", back_populates="pet", cascade="all, delete-orphan"
    )


class Appointment(Base):
    """Cita médica (historial clínico) de una mascota."""

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(String(200), nullable=False)
    diagnosis = Column(Text, nullable=True)
    veterinarian = Column(String(100), nullable=True)
    status = Column(String(20), default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="appointments")
