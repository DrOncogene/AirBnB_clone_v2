#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column('name', String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship('City', back_populates='state')
    else:
        @property
        def cities(self):
            all_cities = storage.all(City)
            state_cities = [v for k, v in all_cities.items()
                            if v.state_id == self.id]
            return state_cities
