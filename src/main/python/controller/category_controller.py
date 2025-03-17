from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.repository.category_repository import CategoryRepository
from src.main.python.transformers.category_transformer import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category_endpoint(category_data: CategoryCreate, db: Session = Depends(get_db)):
    category = CategoryRepository.create_category(db, category_data.dict())
    return category


@router.get("/", response_model=List[CategoryResponse])
def list_categories_endpoint(db: Session = Depends(get_db)):
    return CategoryRepository.list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    category = CategoryRepository.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = CategoryRepository.update_category(db, category_id, category_update.dict(exclude_unset=True))
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", status_code=204)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    deleted_category = CategoryRepository.delete_category(db, category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return
