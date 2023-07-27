from fastapi import APIRouter

from app.api.routes import clients
from app.api.routes import hospitals
from app.api.routes import doctors
from app.api.routes import reviews
from app.api.routes import visits

api_router = APIRouter()

pet_expert_router = APIRouter()
pet_expert_router.include_router(clients.router, prefix="/clients")
pet_expert_router.include_router(hospitals.router, prefix="/hospitals")
pet_expert_router.include_router(doctors.router, prefix="/doctors")
pet_expert_router.include_router(reviews.router, prefix="/reviews")
pet_expert_router.include_router(visits.router, prefix="/visits")
