from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.python.config.DatabaseConfig import engine, Base
from src.main.python.ApplicationProperties import ApplicationProperties
from src.main.python.controller.recipe_controller import router as recipe_router
from src.main.python.controller.ingredient_controller import router as ingredient_router
from src.main.python.controller.recipe_ingredient_controller import router as recipe_ingredient_router
from src.main.python.controller.comment_controller import router as comment_router
from src.main.python.controller.shopping_list_controller import router as shopping_list_router

# Initialize FastAPI app
app = FastAPI(
    title="Recipe Service API",
    description="API for managing recipes, ingredients, and shopping lists",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
Base.metadata.create_all(bind=engine)

# Register controllers
app.include_router(recipe_router)
app.include_router(ingredient_router)
app.include_router(recipe_ingredient_router)
app.include_router(comment_router)
app.include_router(shopping_list_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe Service API"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "Application:app",
        host=ApplicationProperties.APP_HOST,
        port=ApplicationProperties.APP_PORT,
        reload=ApplicationProperties.DEBUG
    )
