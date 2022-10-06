from fastapi import APIRouter
from app.api import *


# routes
router = APIRouter()
router.include_router(addresses_router)