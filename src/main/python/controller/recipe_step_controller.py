from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services.recipe_step_service import (
    create_recipe_step,
    list_steps_by_recipe,
    get_recipe_step,
    update_recipe_step,
    delete_recipe_step
)
from src.main.python.transformers.recipe_step_transformer import (
    RecipeStepCreate,
    RecipeStepUpdate,
    RecipeStepResponse
)

router = APIRouter(prefix="/recipes/{recipe_id}/steps", tags=["Recipe Steps"])


@router.post("/", response_model=RecipeStepResponse)
def create_step_endpoint(
    recipe_id: int,
    step_data: RecipeStepCreate,
    db: Session = Depends(get_db)
):
    new_step = create_recipe_step(db, recipe_id, step_data)
    if not new_step:
        raise HTTPException(status_code=400, detail="Could not create recipe step")
    return new_step


@router.get("/", response_model=List[RecipeStepResponse])
def list_recipe_steps_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    steps = list_steps_by_recipe(db, recipe_id)
    if not steps:
        raise HTTPException(status_code=404, detail="No steps found for this recipe")
    return steps


@router.get("/{step_id}", response_model=RecipeStepResponse)
def get_recipe_step_endpoint(
    recipe_id: int,
    step_id: int,
    db: Session = Depends(get_db)
):
    step = get_recipe_step(db, recipe_id, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found for this recipe")
    return step


@router.put("/{step_id}", response_model=RecipeStepResponse)
def update_recipe_step_endpoint(
    recipe_id: int,
    step_id: int,
    step_update: RecipeStepUpdate,
    db: Session = Depends(get_db)
):
    updated_step = update_recipe_step(db, recipe_id, step_id, step_update)
    if not updated_step:
        raise HTTPException(status_code=404, detail="Step not found or not updated")
    return updated_step


@router.delete("/{step_id}", status_code=204)
def delete_recipe_step_endpoint(
    recipe_id: int,
    step_id: int,
    db: Session = Depends(get_db)
):
    deleted_step = delete_recipe_step(db, recipe_id, step_id)
    if not deleted_step:
        raise HTTPException(status_code=404, detail="Step not found for this recipe")
    return
