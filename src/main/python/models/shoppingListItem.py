from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_item"

    item_id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_list.shopping_list_id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.ingredient_id"))
    quantity = Column(Float, nullable=False)

    shopping_list = relationship("ShoppingList", back_populates="items")
