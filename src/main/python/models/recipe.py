from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.main.python.models import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    duration = Column(Integer)
    meal_type = Column(String(100))
    total_servings = Column(Integer)
    author_user_id = Column(Integer)

    # NEW: Foreign key to Category
    category_id = Column(Integer, ForeignKey("categories.category_id"))

    # Relationship back to Category
    category = relationship("Category", back_populates="recipes")

    # Relationship to ingredients (unchanged)
    ingredients = relationship("Ingredient", back_populates="recipe")

    # Relationship to comments (unchanged)
    comments = relationship("Comment", back_populates="recipe")

    # NEW: Relationship to the step-by-step instructions table
    steps = relationship("RecipeStep", back_populates="recipe", cascade="all, delete-orphan")
