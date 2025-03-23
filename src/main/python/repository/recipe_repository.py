from sqlalchemy.orm import Session
from src.main.python.models.recipe import Recipe

class RecipeRepository:
    @staticmethod
    def create_recipe(db: Session, recipe_data: dict):
        new_recipe = Recipe(**recipe_data)
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: int):
        return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    @staticmethod
    def list_recipes(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Recipe).offset(skip).limit(limit).all()

    @staticmethod
    def update_recipe(db: Session, recipe_id: int, recipe_update: dict):
        recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
        if recipe:
            for key, value in recipe_update.items():
                setattr(recipe, key, value)
            db.commit()
            db.refresh(recipe)
        return recipe

    @staticmethod
    def delete_recipe(db: Session, recipe_id: int):
        recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
        if recipe:
            db.delete(recipe)
            db.commit()
        return recipe

    @staticmethod
    def get_recipes_by_keycloak_user_id(db: Session, keycloak_user_id: str):
        return db.query(Recipe).filter(Recipe.keycloak_user_id == keycloak_user_id).all()

