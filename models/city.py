#!/usr/bin/python3
""" City Module for HBNB project """
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(
                          String(60),
                          ForeignKey('states.id', ondelete='CASCADE'),
                          nullable=False
                         )
        places = relationship('Place', cascade='all, delete',
                              back_populates='cities')
        state = relationship('State', back_populates='cities')
    else:
        state_id = ""
        name = ""
