
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Different requests -> Different Models 
# Schema/Pydantic Model -> This is importante in order to guarantee our database shape
#                          the schema defines the strucutre of a request & response.

# Next two classes handles user sending data to us
class PostBase(BaseModel):
    
    #This is my schema of my DataBank
    # and it is also used to validate the request that will be done by a client
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    #it will inherit from PostBase    
    pass

#Next two classes handles how the system sends data to the user

class PostResponse(PostBase):
    
    #id: int
    #created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    
    email:EmailStr
    password: str
    