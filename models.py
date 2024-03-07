from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hashed = Column(String(255), nullable=False)
    user_token = Column(String(255))

    folders = relationship("Folder", backref="owner")

class Folder(Base):
    __tablename__ = 'folders'
    
    folder_id = Column(String(255), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    