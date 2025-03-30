from sqlalchemy.orm import Session
from src.main.python.repository.comment_repository import CommentRepository
from src.main.python.transformers.comment_transformer import CommentCreate

def add_comment_to_recipe(db: Session, recipe_id: int, comment_data: CommentCreate):
    return CommentRepository.add_comment_to_recipe(
        db, recipe_id, comment_data.dict()
    )

def get_recipe_comments(db: Session, recipe_id: int):
    return CommentRepository.get_recipe_comments(db, recipe_id)

def delete_comment(db: Session, comment_id: int):
    return CommentRepository.delete_comment(db, comment_id)
