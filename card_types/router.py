from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from .models import Type
from data.db import get_async_session
from .schemas import CreateType


router = APIRouter(
    prefix='/card_types',
    tags=['Card Types']
)


@router.get('/')
async def get_styles(session: AsyncSession = Depends(get_async_session)):
    query = select(Type)
    result = await session.execute(query)
    return result.all()


@router.post('/')
async def create_style(new_deck: CreateType, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Type).values(**new_deck.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}