from fastapi import APIRouter

from api.web.api.auth import google
from api.web.api.auth import jwt

router = APIRouter()
router.include_router(google.router, prefix="/google", tags=["GoogleAuth"])
router.include_router(jwt.router, prefix="/jwt", tags=["jwtAuth"])
