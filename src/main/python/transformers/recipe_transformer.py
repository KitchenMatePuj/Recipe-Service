from pydantic import BaseModel
from typing import Optional, List
import datetime

from pydantic import BaseModel
from datetime import datetime

class RecipeRequest(BaseModel):
    category_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    cooking_time: int
    food_type: str
    total_portions: int
    keycloak_user_id: str
    rating_avg: float = 0.0
    image_url: Optional[str] = None


class RecipeResponse(BaseModel):
    recipe_id: int
    category_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    cooking_time: int
    food_type: str
    total_portions: int
    keycloak_user_id: str
    rating_avg: float
    image_url: Optional[str] = None

class FullIngredient(BaseModel):
    ingredient_id: int
    name: str
    measurement_unit: str

class FullStep(BaseModel):
    recipe_step_id: int
    step_number: int
    title: str
    description: str

class FullComment(BaseModel):
    comment_id: int
    author_user_id: str
    rating: Optional[float]
    text: str
    created_at: datetime

class FullRecipeResponse(BaseModel):
    # --- datos básicos de la receta ------------
    recipe_id: int
    category_id: int
    title: str
    cooking_time: int
    food_type: str
    total_portions: int
    keycloak_user_id: str
    rating_avg: float
    image_url: Optional[str]

        # --- anidados ------------------------------
    steps: List[FullStep]
    ingredients: List[FullIngredient]
    comments: List[FullComment]


    class Config:
        orm_mode = True

class RecipeSearchRequest(BaseModel):
    title: Optional[str] = None
    cooking_time: Optional[int] = None
    ingredient: Optional[str] = None