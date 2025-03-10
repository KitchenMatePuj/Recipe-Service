from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    measurement_unit = Column(String(50), nullable=False)

    recipes = relationship("RecipeIngredient", back_populates="ingredient")
