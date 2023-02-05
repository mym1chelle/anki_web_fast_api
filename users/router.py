from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User, UserManager, get_current_active_user
from data.db import get_async_session

from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import UserRead, Token, UserCreate


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
async def get_users(session: AsyncSession = Depends(get_async_session), user=Depends(get_current_active_user)):
    print(user.username)
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/registration/')
async def create_user(new_user: UserCreate, session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Регистрация пользователя"""
    async with session.begin():
        user_manager = UserManager(session)
        user = await user_manager.create_user(
            username=new_user.username,
            password=new_user.password
        )
        return UserRead(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
            decks=[]
        )


@router.post("/token/", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """Получение токена Bearer"""
    user = await UserManager(session=session).authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_active_user)):
    return current_user

