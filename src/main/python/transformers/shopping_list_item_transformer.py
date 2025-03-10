from pydantic import BaseModel

class ShoppingListItemBase(BaseModel):
    ingredient_id: int
    quantity: float

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemResponse(ShoppingListItemBase):
    shopping_list_id: int
    item_id: int

    class Config:
        orm_mode = True
