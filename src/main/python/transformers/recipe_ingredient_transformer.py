from pydantic import BaseModel

class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientResponse(RecipeIngredientBase):
    recipe_id: int

    class Config:
        orm_mode = True
