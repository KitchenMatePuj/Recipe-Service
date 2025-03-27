from sqlalchemy.orm import Session
from src.main.python.repository.category_repository import CategoryRepository
from src.main.python.transformers.category_transformer import CategoryCreate, CategoryUpdate

def create_category(db: Session, category_data: CategoryCreate):
    return CategoryRepository.create_category(db, category_data.dict())

def get_category(db: Session, category_id: int):
    return CategoryRepository.get_category(db, category_id)

def list_categories(db: Session, skip: int = 0, limit: int = 10):
    return CategoryRepository.list_categories(db, skip, limit)

def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    return CategoryRepository.update_category(db, category_id, category_update.dict(exclude_unset=True))

def delete_category(db: Session, category_id: int):
    return CategoryRepository.delete_category(db, category_id)
