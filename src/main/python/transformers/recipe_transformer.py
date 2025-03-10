from pydantic import BaseModel
from typing import Optional
import datetime

class RecipeBase(BaseModel):
    title: str
    instructions: str
    hashtags: Optional[str] = None
    rating: Optional[float] = None
    duration: Optional[int] = None
    meal_type: Optional[str] = None
    cuisine_type: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    total_servings: Optional[int] = None
    author_user_id: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    title: Optional[str] = None
    instructions: Optional[str] = None

class RecipeResponse(RecipeBase):
    recipe_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
