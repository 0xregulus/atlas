from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..config import get_settings
from ..security import create_access_token, verify_password
from ..services.auth import get_admin_user

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
def login(req: LoginRequest) -> dict[str, str]:
    user = get_admin_user(req.username)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(req.username)
    return {"access_token": token, "token_type": "bearer"}
