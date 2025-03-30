from typing import List

from sqlalchemy.orm import Session
from src.main.python.models.recipe import Recipe
from src.main.python.rabbit.rabbit_sender import rabbit_client
from src.main.python.transformers.recipe_transformer import RecipeRequest, RecipeResponse, RecipeSearchRequest
from src.main.python.rabbit.events.recipe_events import build_recipe_event
from src.main.python.repository.recipe_repository import RecipeRepository


async def create_recipe(db: Session, recipe_data: RecipeRequest):
    return await RecipeRepository.create_recipe(db, recipe_data.dict(exclude_unset=True))


def get_recipe(db: Session, recipe_id: int):
    return RecipeRepository.get_recipe(db, recipe_id)


def list_recipes(db: Session, skip: int = 0, limit: int = 10):
    return RecipeRepository.list_recipes(db, skip=skip, limit=limit)


async def update_recipe(db: Session, recipe_id: int, recipe_update: RecipeRequest):
    return await RecipeRepository.update_recipe(db, recipe_id, recipe_update.dict(exclude_unset=True))


async def delete_recipe(db: Session, recipe_id: int):
    return await RecipeRepository.delete_recipe(db, recipe_id)



def get_recipes_by_user(db: Session, keycloak_user_id: str):
    recipes = RecipeRepository.get_recipes_by_keycloak_user_id(db, keycloak_user_id)
    return [RecipeResponse.model_validate(recipe, from_attributes=True) for recipe in recipes]


def get_recipes_by_rating(db: Session, min_rating: float, max_rating: float):
    recipes = RecipeRepository.get_recipes_by_rating_range(db, min_rating, max_rating)
    return [RecipeResponse.model_validate(recipe, from_attributes=True) for recipe in recipes]

def get_recipe_counts_by_cooking_time(db: Session):
    results = RecipeRepository.count_recipes_by_cooking_time(db)
    return [{"cooking_time": row.cooking_time, "count": row.count} for row in results]

def get_total_recipe_count(db: Session):
    return {"total_recipes": RecipeRepository.count_total_recipes(db)}


def search_recipes_service(
    db: Session, search_params: RecipeSearchRequest
) -> List[RecipeResponse]:
    recipes = RecipeRepository.search_recipes(
        db,
        title=search_params.title,
        cooking_time=search_params.cooking_time,
        ingredient=search_params.ingredient
    )
    return [RecipeResponse.model_validate(recipe, from_attributes=True) for recipe in recipes]
