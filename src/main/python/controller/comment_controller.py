from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.main.python.config.DatabaseConfig import get_db
from src.main.python.services.comment_service import (
    add_comment_to_recipe,
    get_recipe_comments,
    delete_comment
)
from src.main.python.transformers.comment_transformer import CommentCreate, CommentResponse

router = APIRouter(prefix="/recipes/{recipe_id}/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def add_comment_endpoint(recipe_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    return add_comment_to_recipe(db, recipe_id, comment_data)

@router.get("/", response_model=List[CommentResponse])
def get_recipe_comments_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    return get_recipe_comments(db, recipe_id)

@router.delete("/{comment_id}", status_code=204)
def delete_comment_endpoint(comment_id: int, db: Session = Depends(get_db)):
    deleted_comment = delete_comment(db, comment_id)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return
