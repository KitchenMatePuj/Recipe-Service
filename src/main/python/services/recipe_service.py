from http.client import HTTPException
from typing import List

from sqlalchemy.orm import Session
from starlette import status

from src.main.python.models import recipe
from src.main.python.models.recipe import Recipe
from src.main.python.rabbit.rabbit_sender import rabbit_client
from src.main.python.transformers.recipe_transformer import RecipeRequest, RecipeResponse, RecipeSearchRequest, \
    FullRecipeResponse
from src.main.python.rabbit.events.recipe_events import build_recipe_event
from src.main.python.repository.recipe_repository import RecipeRepository
from src.main.python.utils.responses import fix_encoding


async def create_recipe(db: Session, recipe_data: RecipeRequest):
    recipe_data.title = fix_encoding(recipe_data.title)
    new_recipe = await RecipeRepository.create_recipe(db, recipe_data.dict(exclude_unset=True))
    print(f"🟢 [SERVICE] recipe.title = {recipe_data.title} → {list(recipe_data.title.encode('utf-8'))}")

    return RecipeResponse.model_validate(new_recipe, from_attributes=True)


def get_recipe(db: Session, recipe_id: int):
    return RecipeRepository.get_recipe(db, recipe_id)


def list_recipes(db: Session, skip: int = 0, limit: int = 10):
    return RecipeRepository.list_recipes(db, skip=skip, limit=limit)


async def update_recipe(
    db: Session,
    recipe_id: int,
    recipe_update: RecipeRequest            # si usas un esquema distinto, cámbialo
) -> RecipeResponse | None:
    recipe_update.title = fix_encoding(recipe_update.title)# ⬅ devuelve el DTO de salida
    updated = await RecipeRepository.update_recipe(
        db,
        recipe_id,
        recipe_update.dict(exclude_unset=True),
    )
    # `update_recipe` ya devuelve el DTO; no hace falta transformar de nuevo
    return updated


async def delete_recipe(db: Session, recipe_id: int):
    return await RecipeRepository.delete_recipe(db, recipe_id)

def get_full_recipe(db: Session, recipe_id: int) -> FullRecipeResponse:
    rec = RecipeRepository.get_full_recipe(db, recipe_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe {recipe_id} not found"
        )
    return FullRecipeResponse.model_validate(rec, from_attributes=True)

def get_recipes_by_user(db: Session, keycloak_user_id: str):
    recipes = RecipeRepository.get_recipes_by_keycloak_user_id(db, keycloak_user_id)
    for r in recipes:
        r.title = fix_encoding(r.title)
    return [RecipeResponse.model_validate(r, from_attributes=True) for r in recipes]


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
