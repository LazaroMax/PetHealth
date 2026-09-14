from fastapi import FastAPI

from .database import Base, engine
from .routers import appointments, auth, owners, pets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PetHealth API",
    description="Sistema de gestión veterinaria: propietarios, mascotas y citas médicas.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(owners.router)
app.include_router(pets.router)
app.include_router(appointments.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "PetHealth API"}
