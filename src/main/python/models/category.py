from sqlalchemy import Column, Integer, String, ForeignKey
from src.main.python.models import Base

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    recipe_id = Column(Integer, ForeignKey("recipe.recipe_id"))
