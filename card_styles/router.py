from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from .models import Style
from data.db import get_async_session
from .schemas import CreateStyle


router = APIRouter(
    prefix='/card_styles',
    tags=['Card Styles']
)


@router.get('/')
async def get_styles(session: AsyncSession = Depends(get_async_session)):
    query = select(Style)
    result = await session.execute(query)
    return result.all()


@router.post('/')
async def create_style(new_deck: CreateStyle, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Style).values(**new_deck.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}