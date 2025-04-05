from pydantic import BaseModel
from typing import Optional
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

    class Config:
        orm_mode = True

class RecipeSearchRequest(BaseModel):
    title: Optional[str] = None
    cooking_time: Optional[int] = None
    ingredient: Optional[str] = None