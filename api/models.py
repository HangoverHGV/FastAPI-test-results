from database import Base
from sqlalchemy import Column, Integer, String


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    ingredients = Column(String)
    steps = Column(String)
    time = Column(Integer)
    difficulty = Column(Integer)
    servings = Column(Integer)
