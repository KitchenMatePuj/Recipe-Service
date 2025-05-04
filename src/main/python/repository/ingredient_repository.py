import asyncio

from sqlalchemy.orm import Session
from src.main.python.models.ingredient import Ingredient
from src.main.python.rabbit.events.recipe_events import build_ingredient_event
from src.main.python.rabbit.rabbit_sender import rabbit_client


class IngredientRepository:
    @staticmethod
    async def create_ingredient(db: Session, ingredient_data: dict):
        new_ingredient = Ingredient(**ingredient_data)
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)

        message = build_ingredient_event(new_ingredient, "ingredient_created")
        await rabbit_client.send_message(message)

        return new_ingredient

    @staticmethod
    def get_ingredient(db: Session, ingredient_id: int):
        return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

    @staticmethod
    def list_ingredients(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Ingredient).offset(skip).limit(limit).all()

    @staticmethod
    async def update_ingredient(db: Session, ingredient_id: int, ingredient_update: dict):
        ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient:
            for key, value in ingredient_update.items():
                setattr(ingredient, key, value)
            db.commit()
            db.refresh(ingredient)

            message = build_ingredient_event(ingredient, "ingredient_updated")
            await rabbit_client.send_message(message)
        return ingredient

    @staticmethod
    async def delete_ingredient(db: Session, ingredient_id: int):
        ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient:
            db.delete(ingredient)
            db.commit()
            message = build_ingredient_event(ingredient, "ingredient_deleted")
            await rabbit_client.send_message(message)
        return ingredient

    @staticmethod
    def get_ingredients_by_recipe(db: Session, recipe_id: int):
        return db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).all()