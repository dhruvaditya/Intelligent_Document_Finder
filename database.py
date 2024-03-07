from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 
URL_DATABASE = 'postgresql://postgres:Post123@localhost/IDF'
engine=create_engine(URL_DATABASE)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()