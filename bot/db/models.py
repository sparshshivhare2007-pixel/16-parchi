"""
SQLAlchemy models.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    score = Column(Integer, default=0)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    host_id = Column(Integer, nullable=False)
    status = Column(String, default="waiting")   # waiting | running | finished
    created_at = Column(DateTime, default=datetime.utcnow)

    parchis = relationship("Parchi", back_populates="game")


class Parchi(Base):
    __tablename__ = "parchis"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    owner_id = Column(Integer, nullable=False)     # who holds it
    naam = Column(String, nullable=False)          # whose name is on it
    number = Column(Integer, nullable=False)       # 1..4

    game = relationship("Game", back_populates="parchis")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    points = Column(Integer, default=0)
