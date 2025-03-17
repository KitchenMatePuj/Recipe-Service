from sqlalchemy.orm import Session
from src.main.python.models.ingredient import Ingredient

class IngredientRepository:
    @staticmethod
    def create_ingredient(db: Session, ingredient_data: dict):
        new_ingredient = Ingredient(**ingredient_data)
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient

    @staticmethod
    def get_ingredient(db: Session, ingredient_id: int):
        return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

    @staticmethod
    def list_ingredients(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Ingredient).offset(skip).limit(limit).all()

    @staticmethod
    def update_ingredient(db: Session, ingredient_id: int, ingredient_update: dict):
        ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient:
            for key, value in ingredient_update.items():
                setattr(ingredient, key, value)
            db.commit()
            db.refresh(ingredient)
        return ingredient

    @staticmethod
    def delete_ingredient(db: Session, ingredient_id: int):
        ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient:
            db.delete(ingredient)
            db.commit()
        return ingredient
