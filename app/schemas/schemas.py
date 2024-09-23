# schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class BlogPostBase(BaseModel):
    title: str
    content: str
    author: str
    image_url: str

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BlogPostPage(BaseModel):
    posts: List[BlogPost]
    total: int
    page: int
    per_page: int
    total_pages: int




