import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from src.main.python.config.DatabaseConfig import engine
from src.main.python.middlewares.log_body import LogRequestBody
from src.main.python.models import Base


from src.main.python.controller.comment_controller import router as comment_router
from src.main.python.controller.ingredient_controller import router as ingredient_router
from src.main.python.controller.category_controller import router as category_router
from src.main.python.controller.recipe_controller import router as recipe_router
from src.main.python.controller.recipe_step_controller import router as recipe_step_router
from src.main.python.utils.responses import UTF8JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Application API",
    description="A simple API for managing recipes, categories, ingredients, and comments.",
    version="1.0.0",
    default_response_class=UTF8JSONResponse
)

app.add_middleware(LogRequestBody)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comment_router)
app.include_router(ingredient_router)
app.include_router(category_router)
app.include_router(recipe_router)
app.include_router(recipe_step_router)
