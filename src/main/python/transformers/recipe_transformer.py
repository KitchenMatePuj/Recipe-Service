from pydantic import BaseModel
from typing import Optional
import datetime

class RecipeBase(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    meal_type: Optional[str] = None
    total_servings: Optional[int] = None
    author_user_id: Optional[int] = None

class RecipeCreate(RecipeBase):
    title: str
    author_user_id: int

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    meal_type: Optional[str] = None
    total_servings: Optional[int] = None
    author_user_id: Optional[int] = None

class RecipeResponse(RecipeBase):
    recipe_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True