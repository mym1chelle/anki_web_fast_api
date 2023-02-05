from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func
from datetime import datetime

from .models import Deck
from cards.models import Card
from data.db import get_async_session
from .schemas import CreateDeck
from users.models import get_current_active_user


router = APIRouter(
    prefix='/decks',
    tags=['Decks']
)


@router.get('/')
async def get_decks(
        session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    query = select(Deck).where(Deck.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/add/')
async def create_deck(
        new_deck: CreateDeck,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    deck_data = new_deck.dict()
    deck_data['user_id'] = user.id
    statement = insert(Deck).values(**deck_data)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.get('/{id}/')
async def get_all_card_in_deck(
        id: int, session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    query = select(Card).where(Card.deck_id == int(id)).where(Card.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/study')
async def get_deck_to_study(
        session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    """Вернет список колод в которых карточки удовлетворяют заданному фильтру"""
    all_count = func.count(Card.id).label('all_cards')
    query = select(
        Deck.name,
        func.count(Card.id).filter(Card.review_date.is_(None)).label('new_cards'),
        func.count(Card.id).filter(Card.review_date <= datetime.now()).label('old_cards'),
    ).join(Card, isouter=True).where(Deck.user_id == user.id).group_by(Deck.id, Deck.name).having(all_count > 0)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/{id}/study_cards/')
async def get_cards_to_study(
        id: int, session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_active_user)
):
    query = select(Card).where(
        Card.deck_id == int(id)
    ).where(Card.review_date.is_(None) | Card.review_date <= datetime.now()).order_by(Card.random_num).limit(1)
    result = await session.execute(query)
    return result.scalars().all()