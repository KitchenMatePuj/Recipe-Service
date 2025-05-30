from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services import ingredient_service
from src.main.python.services.ingredient_service import (
    create_ingredient,
    get_ingredient,
    list_ingredients,
    update_ingredient,
    delete_ingredient
)
from src.main.python.transformers.ingredient_transformer import IngredientCreate, IngredientUpdate, IngredientResponse

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.post("/", response_model=IngredientResponse)
async def create_ingredient_endpoint(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    return await create_ingredient(db, ingredient)


@router.get("/", response_model=List[IngredientResponse])
def list_ingredients_endpoint(db: Session = Depends(get_db)):
    return list_ingredients(db)


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient_endpoint(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = get_ingredient(db, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient_endpoint(ingredient_id: int, ingredient_update: IngredientUpdate, db: Session = Depends(get_db)):
    updated_ingredient = update_ingredient(db, ingredient_id, ingredient_update)
    if not updated_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return await updated_ingredient


@router.delete("/{ingredient_id}", status_code=204)
async def delete_ingredient_endpoint(ingredient_id: int, db: Session = Depends(get_db)):
    deleted_ingredient = await delete_ingredient(db, ingredient_id)
    if not deleted_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return

@router.get("/by-recipe/{recipe_id}", response_model=List[IngredientResponse])
def get_ingredients_by_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    return ingredient_service.get_ingredients_by_recipe(db, recipe_id)