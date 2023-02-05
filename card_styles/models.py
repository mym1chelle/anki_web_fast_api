from sqlalchemy import Column, Integer, String, DateTime
import datetime
from data.db import Base


class Style(Base):
    __tablename__ = 'styles'

    id = Column('id', Integer, primary_key=True, index=True)
    name = Column('name', String, nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.datetime.utcnow)
