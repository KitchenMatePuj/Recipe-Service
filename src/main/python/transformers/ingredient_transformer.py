from pydantic import BaseModel
from typing import Optional

class IngredientBase(BaseModel):
    name: str
    measurement_unit: str
    

class IngredientCreate(IngredientBase):
    recipe_id: int

class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    measurement_unit: Optional[str] = None

class IngredientResponse(IngredientBase):
    recipe_id: Optional[int] = None
    ingredient_id: int

    class Config:
        orm_mode = True
