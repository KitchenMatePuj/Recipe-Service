from sqlalchemy.orm import Session
from src.main.python.models.recipe_step import RecipeStep
from src.main.python.transformers.recipe_step_transformer import RecipeStepCreate, RecipeStepUpdate

def create_recipe_step(db: Session, recipe_id: int, step_data: RecipeStepCreate):
    new_step = RecipeStep(
        recipe_id=recipe_id,
        step_number=step_data.step_number,
        description=step_data.description,
    )
    db.add(new_step)
    db.commit()
    db.refresh(new_step)
    return new_step

def list_steps_by_recipe(db: Session, recipe_id: int):
    return db.query(RecipeStep).filter(RecipeStep.recipe_id == recipe_id).order_by(RecipeStep.step_number).all()

def get_recipe_step(db: Session, recipe_id: int, step_id: int):
    return db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()

def update_recipe_step(db: Session, recipe_id: int, step_id: int, step_update: RecipeStepUpdate):
    step = db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()

    if not step:
        return None

    # Apply updates
    if step_update.step_number is not None:
        step.step_number = step_update.step_number
    if step_update.description is not None:
        step.description = step_update.description

    db.commit()
    db.refresh(step)
    return step

def delete_recipe_step(db: Session, recipe_id: int, step_id: int):
    step = db.query(RecipeStep).filter(
        RecipeStep.recipe_step_id == step_id,
        RecipeStep.recipe_id == recipe_id
    ).first()
    if step:
        db.delete(step)
        db.commit()
        return step
    return None
