# application.py

from fastapi import FastAPI
from src.main.python.config.DatabaseConfig import engine
from src.main.python.models import Base
from src.main.python.controller.comment_controller import router as comment_router
from src.main.python.controller.ingredient_controller import router as ingredient_router
from src.main.python.controller.category_controller import router as category_router
from src.main.python.controller.recipe_controller import router as recipe_router


# Create all tables if they don't exist (Optional if using Alembic or other migrations)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Recipe Application API",
    description="A simple API for managing recipes, categories, ingredients, and comments.",
    version="1.0.0",
)

# Include your routers
app.include_router(comment_router)
app.include_router(ingredient_router)
app.include_router(category_router)
app.include_router(recipe_router)
app.include_router(recipe_router)

@app.get("/")
def root():
    return {"message": "API is up and running!"}
