from sqlalchemy.orm import Session
from src.main.python.transformers.ingredient_transformer import IngredientCreate, IngredientUpdate
from src.main.python.repository.ingredient_repository import IngredientRepository


async def create_ingredient(db: Session, ingredient_data: IngredientCreate):
    return await IngredientRepository.create_ingredient(db, ingredient_data.dict())


def get_ingredient(db: Session, ingredient_id: int):
    return IngredientRepository.get_ingredient(db, ingredient_id)


def list_ingredients(db: Session, skip: int = 0, limit: int = 10):
    return IngredientRepository.list_ingredients(db, skip, limit)


async def update_ingredient(db: Session, ingredient_id: int, ingredient_update: IngredientUpdate):
    return await IngredientRepository.update_ingredient(db, ingredient_id, ingredient_update.dict(exclude_unset=True))


async def delete_ingredient(db: Session, ingredient_id: int):
    return await IngredientRepository.delete_ingredient(db, ingredient_id)

def get_ingredients_by_recipe(db: Session, recipe_id: int):
    return IngredientRepository.get_ingredients_by_recipe(db, recipe_id)
