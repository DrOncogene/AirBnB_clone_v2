#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column('name', String(128), nullable=False)
        cities = relationship('City', back_populates='state',
                              cascade="all, delete")
    else:
        name = ""

        @property
        def cities(self):
            all_cities = models.storage.all(City)
            state_cities = [v for k, v in all_cities.items()
                            if v.state_id == self.id]
            return state_cities
