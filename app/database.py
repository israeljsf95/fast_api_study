# file that will handle the database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

#databank url: databankkind://user:pasw@ip/user/database_name
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/fastapi_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()