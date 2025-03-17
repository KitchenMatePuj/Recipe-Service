from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    measurement_unit = Column(String(50), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))