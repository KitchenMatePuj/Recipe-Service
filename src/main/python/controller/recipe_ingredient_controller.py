from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services.recipe_ingredient_service import (
    add_ingredient_to_recipe,
    get_recipe_ingredients,
    remove_ingredient_from_recipe
)
from src.main.python.transformers.recipe_ingredient_transformer import RecipeIngredientCreate, RecipeIngredientResponse

router = APIRouter(prefix="/recipes/{recipe_id}/ingredients", tags=["Recipe Ingredients"])

@router.post("/", response_model=RecipeIngredientResponse)
def add_ingredient_endpoint(recipe_id: int, ingredient_data: RecipeIngredientCreate, db: Session = Depends(get_db)):
    return add_ingredient_to_recipe(db, recipe_id, ingredient_data)

@router.get("/", response_model=List[RecipeIngredientResponse])
def get_recipe_ingredients_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    return get_recipe_ingredients(db, recipe_id)

@router.delete("/{ingredient_id}", status_code=204)
def remove_ingredient_endpoint(recipe_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    deleted_relation = remove_ingredient_from_recipe(db, recipe_id, ingredient_id)
    if not deleted_relation:
        raise HTTPException(status_code=404, detail="Ingredient not found in recipe")
    return
