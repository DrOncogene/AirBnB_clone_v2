#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id', ondelete='CASCADE'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
