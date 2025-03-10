from sqlalchemy.orm import Session
from src.main.python.models.shoppingList import ShoppingList

class ShoppingListRepository:
    @staticmethod
    def create_shopping_list(db: Session, shopping_list_data: dict):
        new_list = ShoppingList(**shopping_list_data)
        db.add(new_list)
        db.commit()
        db.refresh(new_list)
        return new_list

    @staticmethod
    def get_shopping_list(db: Session, shopping_list_id: int):
        return db.query(ShoppingList).filter(ShoppingList.shopping_list_id == shopping_list_id).first()

    @staticmethod
    def delete_shopping_list(db: Session, shopping_list_id: int):
        shopping_list = db.query(ShoppingList).filter(ShoppingList.shopping_list_id == shopping_list_id).first()
        if shopping_list:
            db.delete(shopping_list)
            db.commit()
        return shopping_list
