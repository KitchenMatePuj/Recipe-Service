from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Photo(Base):
    __tablename__ = "photo"

    photo_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipe.recipe_id", ondelete="CASCADE"), nullable=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_list.shopping_list_id", ondelete="CASCADE"), nullable=True, index=True)

    recipe = relationship("Recipe", back_populates="photos")
    shopping_list = relationship("ShoppingList", back_populates="photos")