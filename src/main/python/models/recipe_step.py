from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class RecipeStep(Base):
    __tablename__ = "recipe_steps"

    recipe_step_id = Column(Integer, primary_key=True, index=True)

    # Which recipe this step belongs to
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)

    # The order of the step, e.g., 1, 2, 3, ...
    step_number = Column(Integer, nullable=False)

    title = Column(String(1000), nullable=False)

    # The step instructions themselves
    description = Column(String(2000), nullable=False)

    # Relationship back to Recipe
    recipe = relationship("Recipe", back_populates="steps")
