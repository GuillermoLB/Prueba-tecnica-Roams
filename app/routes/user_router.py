from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import SessionDep
from app.domain import schemas
from app.repos import user_repo
from app.services.user_service import (authenticate_user,
                                       create_access_token)

settings = Settings()
router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        session: SessionDep,
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, settings=settings)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, session: SessionDep):
    return user_repo.create_user(session, user)
