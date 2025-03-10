from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services.shopping_list_service import (
    create_shopping_list,
    get_shopping_list,
    delete_shopping_list
)
from src.main.python.transformers.shopping_list_transformer import ShoppingListCreate, ShoppingListResponse

router = APIRouter(prefix="/shopping_lists", tags=["Shopping Lists"])

@router.post("/", response_model=ShoppingListResponse)
def create_shopping_list_endpoint(shopping_list_data: ShoppingListCreate, db: Session = Depends(get_db)):
    return create_shopping_list(db, shopping_list_data)

@router.get("/{shopping_list_id}", response_model=ShoppingListResponse)
def get_shopping_list_endpoint(shopping_list_id: int, db: Session = Depends(get_db)):
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    return shopping_list

@router.delete("/{shopping_list_id}", status_code=204)
def delete_shopping_list_endpoint(shopping_list_id: int, db: Session = Depends(get_db)):
    deleted_list = delete_shopping_list(db, shopping_list_id)
    if not deleted_list:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    return
