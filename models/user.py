#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column('email', String(128), nullable=False)
    password = Column('password', String(128), nullable=False)
    first_name = Column('first_name', String(128))
    last_name = Column('last_name', String(128))
    places = relationship('Place', cascade='all, delete', back_populates='user')
    reviews = relationship('Review', cascade='all, delete',
                           back_populates='user')
