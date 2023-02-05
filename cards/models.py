from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
import datetime
from random import randint
from data.db import Base


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    question_type = Column(Integer, ForeignKey('types.id'), nullable=False)
    answer = Column(Text, nullable=False)
    answer_type = Column(Integer, ForeignKey('types.id'), nullable=False)
    style = Column(Integer, ForeignKey('styles.id'), nullable=False)
    deck_id = Column(Integer, ForeignKey('decks.id'), nullable=False)
    deck = relationship('Deck', back_populates="cards")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_by = relationship('User', back_populates="cards")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    easiness = Column(Float)
    interval = Column(Integer)
    repetitions = Column(Integer)
    review_date = Column(DateTime)
    random_num = Column(Integer, default=randint(1, 2000))
