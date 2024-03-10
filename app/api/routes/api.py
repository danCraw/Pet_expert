from fastapi import APIRouter

from app.api.routes import clients
from app.api.routes import hospitals
from app.api.routes import doctors
from app.api.routes import reviews
from app.api.routes import visits
from app.api.routes import replies
from app.api.routes import admin

api_router = APIRouter()

pet_expert_router = APIRouter()
pet_expert_router.include_router(clients.router, prefix="/clients")
pet_expert_router.include_router(hospitals.router, prefix="/hospitals")
pet_expert_router.include_router(doctors.router, prefix="/doctors")
pet_expert_router.include_router(reviews.router, prefix="/reviews")
pet_expert_router.include_router(visits.router, prefix="/visits")
pet_expert_router.include_router(replies.router, prefix="/replies")
pet_expert_router.include_router(admin.router, prefix="/admin")
