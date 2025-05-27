from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class RecipeStep(Base):
    __tablename__ = "recipe_steps"

    recipe_step_id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(1000), nullable=False)
    description = Column(String(2000), nullable=False)

    recipe = relationship("Recipe", back_populates="steps")
