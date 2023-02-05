from sqlalchemy import Column, Integer, String, DateTime
import datetime
from data.db import Base


class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)