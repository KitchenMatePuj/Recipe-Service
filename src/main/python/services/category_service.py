from sqlalchemy.orm import Session
from src.main.python.models.category import Category
from src.main.python.transformers.category_transformer import CategoryCreate, CategoryUpdate

def create_category(db: Session, category_data: CategoryCreate):
    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def list_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category:
        for key, value in category_update.dict(exclude_unset=True).items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category
