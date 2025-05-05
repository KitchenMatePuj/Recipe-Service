from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.main.python.ApplicationProperties import ApplicationProperties

from src.main.python.models.recipe import Recipe
from src.main.python.models.ingredient import Ingredient
from src.main.python.models.comment import Comment
from src.main.python.models.category import Category
from src.main.python.models.recipe_step import RecipeStep


connect_args = (
    {"check_same_thread": False}                     # ← solo si es SQLite
    if "sqlite" in ApplicationProperties.DATABASE_URL
    else {
        "charset": "utf8mb4",
        "init_command": "SET NAMES utf8mb4"
    }
)

engine = create_engine(
    ApplicationProperties.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    encoding="utf8mb4",          # ← refuerzo extra
    connect_args=connect_args
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

Category.__table__.create(bind=engine, checkfirst=True)
Recipe.__table__.create(bind=engine, checkfirst=True)
Ingredient.__table__.create(bind=engine, checkfirst=True)
Comment.__table__.create(bind=engine, checkfirst=True)
RecipeStep.__table__.create(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
