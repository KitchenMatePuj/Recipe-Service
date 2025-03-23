import asyncio

from sqlalchemy.orm import Session
from src.main.python.models.recipe import Recipe
from src.main.python.rabbit.rabbit_sender import rabbit_client
from src.main.python.transformers.recipe_transformer import RecipeRequest, RecipeResponse
from src.main.python.rabbit.events.recipe_events import build_recipe_event
from src.main.python.repository.recipe_repository import RecipeRepository


def create_recipe(db: Session, recipe_data: RecipeRequest):
    new_recipe = Recipe(**recipe_data.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    message = build_recipe_event(new_recipe, "recipe_created")
    asyncio.run(rabbit_client.send_message(message))
    return new_recipe

def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

def list_recipes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Recipe).offset(skip).limit(limit).all()

def update_recipe(db: Session, recipe_id: int, recipe_update: RecipeRequest):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe:
        for key, value in recipe_update.dict(exclude_unset=True).items():
            setattr(recipe, key, value)
        db.commit()
        db.refresh(recipe)
        message = build_recipe_event(recipe, "recipe_updated")
        asyncio.run(rabbit_client.send_message(message))
    return recipe

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe

def get_recipes_by_user(db: Session, keycloak_user_id: str):
    recipes = RecipeRepository.get_recipes_by_keycloak_user_id(db, keycloak_user_id)
    return [RecipeResponse.model_validate(recipe, from_attributes=True) for recipe in recipes]
