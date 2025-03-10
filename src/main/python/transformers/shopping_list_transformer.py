from pydantic import BaseModel
import datetime

class ShoppingListBase(BaseModel):
    user_id: int

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListResponse(ShoppingListBase):
    shopping_list_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
