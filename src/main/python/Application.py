from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- Importar CORS
from src.main.python.config.DatabaseConfig import engine
from src.main.python.middlewares.log_body import LogRequestBody
from src.main.python.models import Base

# Importar tus routers
from src.main.python.controller.comment_controller import router as comment_router
from src.main.python.controller.ingredient_controller import router as ingredient_router
from src.main.python.controller.category_controller import router as category_router
from src.main.python.controller.recipe_controller import router as recipe_router
from src.main.python.controller.recipe_step_controller import router as recipe_step_router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Application API",
    description="A simple API for managing recipes, categories, ingredients, and comments.",
    version="1.0.0",
)

app.add_middleware(LogRequestBody)

# ---------- AÑADIR ESTE BLOQUE PARA HABILITAR CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"], 
    # Agrega aquí las URLs que quieras permitir.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------

# Incluir los routers
app.include_router(comment_router)
app.include_router(ingredient_router)
app.include_router(category_router)
app.include_router(recipe_router)
app.include_router(recipe_step_router)
