import logging

from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from src.main.python.models.ingredient import Ingredient
from src.main.python.models.recipe import Recipe
from src.main.python.rabbit.events.recipe_events import build_recipe_event
from src.main.python.rabbit.rabbit_sender import rabbit_client
from src.main.python.transformers.recipe_transformer import RecipeResponse

class RecipeRepository:
    @staticmethod
    async def create_recipe(db: Session, recipe_data: dict):
            new_recipe = Recipe(**recipe_data)
            print(f"📦 [DAO] Guardando título: {recipe_data['title']} → {list(recipe_data['title'].encode('utf-8'))}")
            db.add(new_recipe)
            db.commit()
            db.refresh(new_recipe)

            message = build_recipe_event(new_recipe, "recipe_created")
            await rabbit_client.send_message(message)

            # recipe_repository.py  (create_recipe)
            logging.warning("💾 [DAO] title = %s", recipe_data["title"])

            return new_recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: int):
        return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    @staticmethod
    def list_recipes(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Recipe).offset(skip).limit(limit).all()

    @staticmethod
    async def update_recipe(db: Session, recipe_id: int, data: dict):
        # ▶︎  localiza la receta
        recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
        if recipe is None:
            return None  # o lanza 404

        # ▶︎  aplica sólo los campos recibidos
        for key, value in data.items():
            setattr(recipe, key, value)

        db.commit()
        db.refresh(recipe)  # ←  ahora recipe.category está poblado

        # ▶︎  publica el evento usando el ORM
        message = build_recipe_event(recipe, "recipe_updated")
        await rabbit_client.send_message(message)

        # ▶︎  devuelve el DTO que espera FastAPI
        return RecipeResponse.model_validate(recipe, from_attributes=True)

    @staticmethod
    async def delete_recipe(db: Session, recipe_id: int):
        recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
        if recipe:
            _ = recipe.category.name if recipe.category else None

            message = build_recipe_event(recipe, "recipe_deleted")
            await rabbit_client.send_message(message)

            db.delete(recipe)
            db.commit()

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

    @staticmethod
    def count_recipes_by_cooking_time(db: Session):
        return db.query(
            Recipe.cooking_time,
            func.count(Recipe.recipe_id).label("count")
        ).group_by(Recipe.cooking_time).all()

    @staticmethod
    def count_total_recipes(db: Session):
        return db.query(func.count(Recipe.recipe_id)).scalar()

    @staticmethod
    def search_recipes(db: Session, title: str = None, cooking_time: int = None, ingredient: str = None):
        query = db.query(Recipe)

        if title:
            query = query.filter(Recipe.title.ilike(f"%{title}%"))

        if cooking_time:
            query = query.filter(Recipe.cooking_time == cooking_time)

        if ingredient:
            query = query.join(Recipe.ingredients).filter(Ingredient.name.ilike(f"%{ingredient}%"))

        return query.all()

    @staticmethod
    def get_full_recipe(db: Session, recipe_id: int):
        """Devuelve receta + steps + ingredients + comments en una sola ida."""
        return (
            db.query(Recipe)
            .options(
                selectinload(Recipe.steps),
                selectinload(Recipe.ingredients),
                selectinload(Recipe.comments)
            )
            .filter(Recipe.recipe_id == recipe_id)
            .first()
        )