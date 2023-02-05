import asyncio

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import AsyncClient
from typing import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
import os
import pytest

import sys



sys.path.append(r'/Users/timursamusenko/Desktop/anki_web_fast_api_test')


from main import app
from models import Base
from data.db import get_async_session
from users.models import UserManager, User
from users.schemas import UserInDB

load_dotenv()

SQLALCHEMY_TEST_DATABASE_URL = os.getenv('SQLALCHEMY_TEST_DATABASE_URL')

engine_test = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)
async_session_maker_test = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def create_db():
    async with engine_test.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


async def test_get_user(self, username: str):
    query = select(User).where(User.username == username).options(selectinload(User.decks))
    if not self.session:
        async with async_session_maker_test() as session:
            async with session.begin():
                result = await session.execute(query)
                user = result.scalars().first()
    else:
        result = await self.session.execute(query)
        user = result.scalars().first()
    if user:
        return UserInDB(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
            password=user.password,
            decks=user.decks
            )
    return None

UserManager.get_user = test_get_user
