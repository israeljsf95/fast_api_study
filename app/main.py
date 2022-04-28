
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg2 as pp
from psycopg2.extras import RealDictCursor
import time

# uvicorn app.main:app --reload (this is necessary because the '.' means that we are trying bring )

app = FastAPI()


class Post(BaseModel):
    
    title: str
    content: str
    published: bool = True

while True: 

    try:
        conn = pp.connect(host = "localhost", dbname = "fastapi_db", 
                        user = "postgres", password = "1234",
                        cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("database connection succesfull!!")
        break
    except Exception as error: 
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)
    
my_posts  = [{"title": "titulo 1", "content": "conteudo 1", "id": 1},
             {"title": "titulo 2", "content": "conteudo 2", "id": 2}]

def find_post(id):
   for post in my_posts:
       if post['id'] == int(id):
           return post
   return None 

def find_idx(id):
    
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == id: 
            return i
    return None
        

@app.get("/")
def root():
    return {"message": "Hello Mundo"}
    #return {"message": [i for i in range(10)]}

@app.get("/posts")
def get_posts():
    
    #fastapi_project is the name of my table
    query = """ select 
                    * 
                from fastapi_project"""
    cursor.execute(query)
    #getting the posts
    posts = cursor.fetchall()
    return {"data": posts}

#Mudando o Status Code para criação de um post
@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    
    query = """insert into fastapi_project (title, content, published) values (%s, %s, %s) returning * """
    #Good Practice to avoid SQL INJECTION
    #the second parameter will be the variables that will be marked at the %s
    #the order matters
    cursor.execute(query, (post.title, post.content, post.published)) 
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    return {"data": "created post"}

#{id} é um path-parameter
@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    # Validation with  for / path without parameter
    query = """ select 
                    * 
                from fastapi_project 
                where id = %s """
    cursor.execute(query, (str(id)))
    post = cursor.fetchone()
    print(post)
    # post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail = f"post com id: {id} não encontrado")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post com o id: {id} não encontrado"}
    return {"post_detail": post}


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id):
    idx = find_idx(int(id))
    del my_posts[idx]
    print(my_posts)
    return {"message: post foi deletado com sucesso"}