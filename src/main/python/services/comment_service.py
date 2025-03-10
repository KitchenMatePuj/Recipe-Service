from sqlalchemy.orm import Session
from src.main.python.models.comment import Comment
from src.main.python.transformers.comment_transformer import CommentCreate

def add_comment_to_recipe(db: Session, recipe_id: int, comment_data: CommentCreate):
    new_comment = Comment(
        recipe_id=recipe_id,
        author_user_id=comment_data.author_user_id,
        text=comment_data.text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_recipe_comments(db: Session, recipe_id: int):
    return db.query(Comment).filter(Comment.recipe_id == recipe_id).all()

def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
