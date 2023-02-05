from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Card
from decks.models import Deck
from data.db import get_async_session
from .schemas import CreateCard, CardWithCreator
from sqlalchemy.orm import selectinload
from users.models import get_current_active_user


router = APIRouter(
    prefix='/cards',
    tags=['Cards']
)


@router.get('/')
async def get_cards(
        limit: int = 15,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    """Выводит список всех созданных карточек пользователя"""
    query = select(Card).where(Card.user_id == user.id).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/add/')
async def create_card(
        new_card: CreateCard, session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    """Добавление карточки"""
    card_data = new_card.dict()
    card_data['user_id'] = user.id
    deck = await session.execute(
        select(Deck).where(Deck.id == card_data['deck_id'])
    )
    deck = deck.scalars().first()
    if not deck:
        raise HTTPException(
            status_code=422,
            detail='Нельзя добавть карточку в несуществующую колоду'
        )
    card = Card(**card_data)
    session.add(card)
    await session.commit()
    await session.refresh(card)
    return card


@router.get('/{id}/')
async def get_card(id: int, session: AsyncSession = Depends(get_async_session)) -> CardWithCreator:
    """Вывод карточки по индексу с указанием имени пользователя, который создал карточку"""
    result = await session.execute(
        select(Card).where(Card.id == id).options(selectinload(Card.created_by)))
    a = result.scalars().first()
    return CardWithCreator(**a.__dict__)