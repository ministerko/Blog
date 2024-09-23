# main.py

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List
from app.models import models
from app.schemas import schemas
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the exact domains here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize basic authentication
security = HTTPBasic()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password verification function
def verify_password(credentials: HTTPBasicCredentials):
    return credentials.username == "admin" and credentials.password == SECRET_PASSWORD

@app.post("/blog-posts/", response_model=schemas.BlogPost)
def create_blog_post(blog_post: schemas.BlogPostCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if not verify_password(credentials):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    db_blog_post = models.BlogPost(**blog_post.dict())
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.get("/blog-posts/", response_model=List[schemas.BlogPost])
def read_blog_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if not verify_password(credentials):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    blog_posts = db.query(models.BlogPost).offset(skip).limit(limit).all()
    return blog_posts

@app.get("/blog-posts/{post_id}", response_model=schemas.BlogPost)
def read_blog_post(post_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if not verify_password(credentials):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    db_blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog_post

@app.get("/blog-posts-page/", response_model=schemas.BlogPostPage)
def read_blog_posts_page(page: int = 1, per_page: int = 6, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if not verify_password(credentials):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    total = db.query(models.BlogPost).count()
    blog_posts = db.query(models.BlogPost).offset((page - 1) * per_page).limit(per_page).all()
    return {
        "posts": blog_posts,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }
