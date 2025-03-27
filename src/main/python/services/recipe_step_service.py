from sqlalchemy.orm import Session
from src.main.python.repository.recipe_step_repository import RecipeStepRepository
from src.main.python.transformers.recipe_step_transformer import RecipeStepCreate, RecipeStepUpdate


def create_recipe_step(db: Session, recipe_id: int, step_data: RecipeStepCreate):
    return RecipeStepRepository.create_step(db, {
        "recipe_id": recipe_id,
        "step_number": step_data.step_number,
        "description": step_data.description
    })


def list_steps_by_recipe(db: Session, recipe_id: int):
    return RecipeStepRepository.get_steps_by_recipe(db, recipe_id)


def get_recipe_step(db: Session, recipe_id: int, step_id: int):
    steps = RecipeStepRepository.get_steps_by_recipe(db, recipe_id)
    return next((step for step in steps if step.recipe_step_id == step_id), None)


def update_recipe_step(db: Session, recipe_id: int, step_id: int, step_update: RecipeStepUpdate):
    step = get_recipe_step(db, recipe_id, step_id)
    if not step:
        return None

    if step_update.step_number is not None:
        step.step_number = step_update.step_number
    if step_update.description is not None:
        step.description = step_update.description

    db.commit()
    db.refresh(step)
    return step


def delete_recipe_step(db: Session, recipe_id: int, step_id: int):
    step = get_recipe_step(db, recipe_id, step_id)
    if step:
        return RecipeStepRepository.delete_step(db, step.recipe_step_id)
    return None
