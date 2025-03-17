from sqlalchemy.orm import Session
from src.main.python.models.recipe_step import RecipeStep

class RecipeStepRepository:
    @staticmethod
    def create_step(db: Session, step_data: dict):
        new_step = RecipeStep(**step_data)
        db.add(new_step)
        db.commit()
        db.refresh(new_step)
        return new_step

    @staticmethod
    def get_steps_by_recipe(db: Session, recipe_id: int):
        return db.query(RecipeStep).filter(RecipeStep.recipe_id == recipe_id).order_by(RecipeStep.step_number).all()

    @staticmethod
    def delete_step(db: Session, step_id: int):
        step = db.query(RecipeStep).filter(RecipeStep.recipe_step_id == step_id).first()
        if step:
            db.delete(step)
            db.commit()
        return step
