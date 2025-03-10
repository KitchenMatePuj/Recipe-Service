from sqlalchemy.orm import Session
from src.main.python.models.recipeIngredient import RecipeIngredient

class RecipeIngredientRepository:
    @staticmethod
    def add_ingredient_to_recipe(db: Session, recipe_id: int, ingredient_id: int, quantity: float):
        new_relation = RecipeIngredient(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity)
        db.add(new_relation)
        db.commit()
        db.refresh(new_relation)
        return new_relation

    @staticmethod
    def get_recipe_ingredients(db: Session, recipe_id: int):
        return db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()

    @staticmethod
    def remove_ingredient_from_recipe(db: Session, recipe_id: int, ingredient_id: int):
        relation = db.query(RecipeIngredient).filter(
            RecipeIngredient.recipe_id == recipe_id,
            RecipeIngredient.ingredient_id == ingredient_id
        ).first()
        if relation:
            db.delete(relation)
            db.commit()
        return relation
