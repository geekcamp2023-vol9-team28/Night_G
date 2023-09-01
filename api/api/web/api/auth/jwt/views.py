from fastapi import APIRouter, Depends
from api.library.jwt_verify import jwt_verify
from typing import Dict, Union

router = APIRouter()

@router.post("/verify")
async def jwt_verify(result: Dict[str, bool] = Depends(jwt_verify)) -> Dict[str, bool]:
    return result