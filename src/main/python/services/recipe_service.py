from sqlalchemy.orm import Session
from src.main.python.models.recipe import Recipe
from src.main.python.transformers.recipe_transformer import RecipeCreate, RecipeUpdate

def create_recipe(db: Session, recipe_data: RecipeCreate):
    new_recipe = Recipe(**recipe_data.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

def list_recipes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Recipe).offset(skip).limit(limit).all()

def update_recipe(db: Session, recipe_id: int, recipe_update: RecipeUpdate):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe:
        for key, value in recipe_update.dict(exclude_unset=True).items():
            setattr(recipe, key, value)
        db.commit()
        db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe
