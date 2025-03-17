from typing import Optional
from pydantic import BaseModel

# Pydantic v2:
# If you want to enable ORM mode in Pydantic v2, use `from_attributes = True` in the Config.


class RecipeStepCreate(BaseModel):
    step_number: int
    description: str

    class Config:
        from_attributes = True  # Pydantic v2 equivalent of old orm_mode = True


class RecipeStepUpdate(BaseModel):
    step_number: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class RecipeStepResponse(BaseModel):
    recipe_step_id: int
    recipe_id: int
    step_number: int
    description: str

    class Config:
        from_attributes = True
