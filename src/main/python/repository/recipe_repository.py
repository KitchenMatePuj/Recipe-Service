from sqlalchemy.orm import Session
from src.main.python.models.recipe import Recipe
from src.main.python.rabbit.events.recipe_events import build_recipe_event
from src.main.python.rabbit.rabbit_sender import rabbit_client


class RecipeRepository:
    @staticmethod
    async def create_recipe(db: Session, recipe_data: dict):
            new_recipe = Recipe(**recipe_data)
            db.add(new_recipe)
            db.commit()
            db.refresh(new_recipe)

            message = build_recipe_event(new_recipe, "recipe_created")
            await rabbit_client.send_message(message)

            return new_recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: int):
        return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    @staticmethod
    def list_recipes(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Recipe).offset(skip).limit(limit).all()

    @staticmethod
    async def update_recipe(db: Session, recipe_id: int, recipe_update: dict):
            recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
            if recipe:
                for key, value in recipe_update.items():
                    setattr(recipe, key, value)
                db.commit()
                db.refresh(recipe)

                message = build_recipe_event(recipe_update, "recipe_updated")
                await rabbit_client.send_message(message)
            return recipe

    @staticmethod
    async def delete_recipe(db: Session, recipe_id: int):
            recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
            if recipe:
                db.delete(recipe)
                db.commit()
                message = build_recipe_event(recipe_id, "recipe_deleted")
                await rabbit_client.send_message(message)
            return recipe

    @staticmethod
    def get_recipes_by_keycloak_user_id(db: Session, keycloak_user_id: str):
        return db.query(Recipe).filter(Recipe.keycloak_user_id == keycloak_user_id).all()

    @staticmethod
    def get_recipes_by_rating_range(db: Session, min_rating: float, max_rating: float):
        return db.query(Recipe).filter(
            Recipe.rating_avg >= min_rating,
            Recipe.rating_avg <= max_rating
        ).all()


