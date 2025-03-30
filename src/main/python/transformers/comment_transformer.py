from pydantic import BaseModel
from typing import Optional
import datetime

class CommentBase(BaseModel):
    author_user_id: str
    rating: Optional[float] = None
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    comment_id: int
    recipe_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
