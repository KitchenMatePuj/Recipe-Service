from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.models.recipe import Recipe
from src.main.python.models.recipe_step import RecipeStep
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
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    new_step = RecipeStep(
        recipe_id=recipe_id,
        step_number=step_data.step_number,
        title=step_data.title,
        description=step_data.description,
    )
    db.add(new_step)
    db.commit()
    db.refresh(new_step)
    return new_step

@router.get("/", response_model=list[RecipeStepResponse])
def list_recipe_steps_endpoint(
        recipe_id: int,
        db: Session = Depends(get_db)
):
    steps = db.query(RecipeStep).filter(RecipeStep.recipe_id == recipe_id).order_by(RecipeStep.step_number).all()
    return steps

@router.get("/{step_id}", response_model=RecipeStepResponse)
def get_recipe_step_endpoint(
        recipe_id: int,
        step_id: int,
        db: Session = Depends(get_db)
):
    step = db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()

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
    step = db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()

    if not step:
        raise HTTPException(status_code=404, detail="Step not found or not updated")

    if step_update.step_number is not None:
        step.step_number = step_update.step_number
    if step_update.title is not None:
        step.title = step_update.title
    if step_update.description is not None:
        step.description = step_update.description

    db.commit()
    db.refresh(step)
    return step

@router.delete("/{step_id}", status_code=204)
def delete_recipe_step_endpoint(
        recipe_id: int,
        step_id: int,
        db: Session = Depends(get_db)
):
    step = db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()
    if step:
        db.delete(step)
        db.commit()
        return step
    raise HTTPException(status_code=404, detail="Step not found for this recipe")