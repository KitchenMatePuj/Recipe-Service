from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))

    # A category can have multiple recipes referencing it
    recipes = relationship("Recipe", back_populates="category")
