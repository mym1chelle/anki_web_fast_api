from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from data.db import Base


class Deck(Base):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_by = relationship('User', back_populates="decks")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    cards = relationship('Card', back_populates='deck')
