from sqlalchemy.orm import Session
from src.main.python.models.ingredient import Ingredient
from src.main.python.transformers.ingredient_transformer import IngredientCreate, IngredientUpdate

def create_ingredient(db: Session, ingredient_data: IngredientCreate):
    new_ingredient = Ingredient(**ingredient_data.dict())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

def list_ingredients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ingredient).offset(skip).limit(limit).all()

def update_ingredient(db: Session, ingredient_id: int, ingredient_update: IngredientUpdate):
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if ingredient:
        for key, value in ingredient_update.dict(exclude_unset=True).items():
            setattr(ingredient, key, value)
        db.commit()
        db.refresh(ingredient)
    return ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if ingredient:
        db.delete(ingredient)
        db.commit()
    return ingredient
