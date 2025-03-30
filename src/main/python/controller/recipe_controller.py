from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services.recipe_service import (
    create_recipe,
    get_recipe,
    list_recipes,
    update_recipe,
    delete_recipe, get_recipes_by_user, get_recipes_by_rating, get_recipe_counts_by_cooking_time, get_total_recipe_count
)
from src.main.python.transformers.recipe_transformer import RecipeRequest, RecipeResponse

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=RecipeResponse)
async def create_recipe_endpoint(recipe: RecipeRequest, db: Session = Depends(get_db)):
    return await create_recipe(db, recipe)


@router.get("/", response_model=List[RecipeResponse])
def list_recipes_endpoint(db: Session = Depends(get_db)):
    return list_recipes(db)


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe_endpoint(recipe_id: int, recipe_update: RecipeRequest, db: Session = Depends(get_db)):
    updated_recipe = update_recipe(db, recipe_id, recipe_update)
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return await updated_recipe


@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    deleted_recipe = await delete_recipe(db, recipe_id)
    if not deleted_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return

@router.get("/user/{keycloak_user_id}", response_model=List[RecipeResponse])
def list_recipes_by_user(keycloak_user_id: str, db: Session = Depends(get_db)):
    return get_recipes_by_user(db, keycloak_user_id)

@router.get("/ratings/filter", response_model=List[RecipeResponse])
def list_recipes_by_rating(min_rating: float = 4.0, max_rating: float = 5.0, db: Session = Depends(get_db)):
    return get_recipes_by_rating(db, min_rating, max_rating)

@router.get("/statistics/cooking-time")
def recipe_count_by_cooking_time(db: Session = Depends(get_db)):
    return get_recipe_counts_by_cooking_time(db)

@router.get("/statistics/total")
def total_recipe_count(db: Session = Depends(get_db)):
    return get_total_recipe_count(db)


