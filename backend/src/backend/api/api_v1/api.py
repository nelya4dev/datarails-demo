from fastapi import APIRouter
from backend.api.api_v1.endpoints import employees, upload

api_router = APIRouter()
api_router.include_router(employees.router)
api_router.include_router(upload.router)
