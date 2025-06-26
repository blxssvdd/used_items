from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.users import db_actions
from app.db.users.models import User
from app.db.base import get_db
from app.pydantic_models.users import UserModel, UserModelResponse, TokenModel

users_route = APIRouter(prefix="/users", tags=["User"])


@users_route.post("/", status_code=status.HTTP_201_CREATED)
async def sign_up(user_model: UserModel, db: Annotated[AsyncSession, Depends(get_db)]):
    await db_actions.sign_up(**user_model.model_dump(), db=db)



@users_route.post("/token/", status_code=status.HTTP_202_ACCEPTED, response_model=TokenModel)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    return await db_actions.sign_in(username=form_data.username, password=form_data.password, db=db)


@users_route.get("/me/", status_code=status.HTTP_202_ACCEPTED, response_model=UserModelResponse)
async def get_user(username: Annotated[User, Depends(db_actions.decode_jwt)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_user(username=username, db=db)
