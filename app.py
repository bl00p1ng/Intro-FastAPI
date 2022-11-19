from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid


app = FastAPI()

posts = []

# Post Model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    isPublished: bool = False


# RUTAS
@app.get('/')
def read_root():
    return {'hello': 'Hello World!'}


# Obtener todos los posts
@app.get('/posts')
def get_posts():
    return posts


# Obtener un post por su ID
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='Post not found')


# Guardar post
@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]


# Eliminar un post por su ID
@app.delete('/post/{post_id}')
def delete_post(post_id: str):
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(i)
            return {'message': 'The post has been deleted'}
    raise HTTPException(status_code=404, detail='Post not found')


# Actualizar un post por su ID
@app.put('/post/{post_id}')
def update_post(post_id: str, updated_post: Post):
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            posts[i]['title'] = updated_post.title
            posts[i]['content'] = updated_post.content
            posts[i]['author'] = updated_post.author
            return {'message': 'The post has been updated'}
    raise HTTPException(status_code=404, detail='Post not found')
