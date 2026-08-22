from fastapi import APIRouter
from app.api.v1.routers import auth, options, passport, trips

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(options.router)
api_router.include_router(passport.router)
api_router.include_router(trips.router)
