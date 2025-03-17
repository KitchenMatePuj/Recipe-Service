from typing import Optional
from pydantic import BaseModel

class RecipeStepCreate(BaseModel):
    step_number: int
    title: str
    description: str

    class Config:
        from_attributes = True

class RecipeStepUpdate(BaseModel):
    step_number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class RecipeStepResponse(BaseModel):
    recipe_step_id: int
    recipe_id: int
    step_number: int
    title: str
    description: str

    class Config:
        from_attributes = True
