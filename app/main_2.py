
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, final
from random import randrange

import psycopg2 as pp
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

class Post(BaseModel):
    #This is my schema of my DataBank
    title: str
    content: str
    published: bool = True


models.Base.metadata.create_all(bind = engine)

# uvicorn app.main:app --reload (this is necessary because the '.' means that we are trying bring )
# DB Name -> fastapi_db
# DB PAss -> "1234"
app = FastAPI()

while True: 

    try:
        conn = pp.connect(host = "localhost", dbname = "fastapi_db", 
                        user = "postgres", password = "1234",
                        cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("database connection was succesfull!!")
        break
    except Exception as error: 
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)


@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data":posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}

# #Mudando o Status Code para criação de um post
@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #unpacking the dictionary makes our program scalable to match a higher number of columns
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

#{id} é um path-parameter
@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):

    #similar to use where on SQL
    #is possible to use .all() ->, the problem is that the SQLALCHEMY will continue to look at our bank until match every
    #possible entrie that satisfies the condition inside the filter statement. To avoid the overload of this kind of operation
    #, as we know that we have only id by post, it is better change the .all to .first
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()
    print(post)
    
    return {"post_detail": post}


# @app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, ):
#     """ idx = find_idx(int(id))
#     del my_posts[idx]
#     print(my_posts) """
#     query = """ delete from fastapi_project
#                 where id = %s returning *
#              """
#     cursor.execute(query, str(id))
#     deleted_post = cursor.fetchone()
#     if deleted_post == None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found")
#     print(deleted_post)

#     return {"message: post deleted with success"}


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):

#     query = """
#                 update fastapi_project set title = %s, content = %s, published = %s 
#                 where id = %s
#                 returning *
#     """
#     cursor.execute(query, (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found")

#     return {"message: post updated with success"}