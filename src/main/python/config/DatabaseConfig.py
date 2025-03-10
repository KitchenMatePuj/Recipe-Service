from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.main.python.ApplicationProperties import ApplicationProperties

from src.main.python.models.recipe import Recipe
from src.main.python.models.ingredient import Ingredient
from src.main.python.models.recipeIngredient import RecipeIngredient
from src.main.python.models.comment import Comment
from src.main.python.models.category import Category
from src.main.python.models.photo import Photo
from src.main.python.models.shoppingList import ShoppingList
from src.main.python.models.shoppingListItem import ShoppingListItem


engine = create_engine(
    ApplicationProperties.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in ApplicationProperties.DATABASE_URL else {}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

Recipe.__table__.create(bind=engine, checkfirst=True)
ShoppingList.__table__.create(bind=engine, checkfirst=True)
Ingredient.__table__.create(bind=engine, checkfirst=True)
RecipeIngredient.__table__.create(bind=engine, checkfirst=True)
Comment.__table__.create(bind=engine, checkfirst=True)
Category.__table__.create(bind=engine, checkfirst=True)
Photo.__table__.create(bind=engine, checkfirst=True)
ShoppingListItem.__table__.create(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
