from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
import datetime
from sqlalchemy import select
from fastapi import HTTPException
from data.db import Base, async_session_maker, get_async_session
from sqlalchemy.orm import relationship, selectinload
from jose import JWTError, jwt

from .auth import oauth2_scheme, SECRET_KEY, ALGORITHM, verify_password, get_password_hash
from .schemas import TokenData, UserInDB, UserRead

# ОШИБКА В РАБОТЕ С ТЕСТАМИ
# Внутри функции испольщую async_session_maker напрямую не через функцию get_async_session
# поэтому когда в тестах происходит переопределение Depends та часть кода, которая работатет
# с async_session_maker напрямую не переопределяется
# РЕШЕНИЕ
# в тестах использовал Monkey Patching чтобы вызывать тестовый session_maker


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    decks = relationship('Deck', back_populates='created_by')
    cards = relationship('Card', back_populates='created_by')
    password = Column(String, nullable=False)


class UserManager:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def get_user(self, username: str):
        query = select(User).where(User.username == username).options(selectinload(User.decks))  # options для вывода колоды
        if not self.session:
            async with async_session_maker() as session:
                async with session.begin():
                    result = await session.execute(query)
                    user = result.scalars().first()
                    print('User context manager')
        else:
            result = await self.session.execute(query)
            user = result.scalars().first()
            print('Use generator')
        if user:
            return UserInDB(
                id=user.id,
                username=user.username,
                created_at=user.created_at,
                password=user.password,
                decks=user.decks  # для вывода колоды
                )
        return None

    async def create_user(self, username: str, password: str):
        user = await self.get_user(username)
        if user:
            raise HTTPException(status_code=500, detail=f'Пользователь с username {username} уже существует')
        else:
            new_user = User(
                username=username,
                password=get_password_hash(password)
            )
            self.session.add(new_user)
            await self.session.flush()
            return new_user

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(current_user: UserRead = Depends(UserManager().get_current_user)):
    return current_user
