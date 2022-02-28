
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None
    
    
my_posts  = [{"title": "titulo 1",
              "content": "conteudo 1",
              "id": 1},
             {"title": "titulo 2",
              "content": "conteudo 2",
              "id": 2}]

@app.get("/")
def root():
    return {"message": "Hello Mundo"}
    #return {"message": [i for i in range(10)]}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"message": post_dict}

#{id} é um path-parameter
@app.get('/posts/{id}')
def get_post(id):
    print(id)
    return {"post_detail": f"here is post {id}"}

