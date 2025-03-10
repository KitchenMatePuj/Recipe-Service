from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from src.main.python.models import Base

class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    instructions = Column(String(5000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hashtags = Column(String(255))
    rating = Column(Float)
    duration = Column(Integer)
    meal_type = Column(String(100))
    cuisine_type = Column(String(100))
    dietary_restrictions = Column(String(255))
    total_servings = Column(Integer)
    author_user_id = Column(Integer)

    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    comments = relationship("Comment", back_populates="recipe")
    photos = relationship("Photo", back_populates="recipe")
