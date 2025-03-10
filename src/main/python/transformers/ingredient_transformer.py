from pydantic import BaseModel
from typing import Optional

class IngredientBase(BaseModel):
    name: str
    measurement_unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    measurement_unit: Optional[str] = None

class IngredientResponse(IngredientBase):
    ingredient_id: int

    class Config:
        orm_mode = True
