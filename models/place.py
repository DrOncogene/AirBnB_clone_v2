#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
import models
from models.base_model import BaseModel, Base


place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False
                             ),
                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False
                             )
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(
                         String(60),
                         ForeignKey('cities.id', ondelete='CASCADE'),
                         nullable=False
                        )
        user_id = Column(
                         String(60),
                         ForeignKey('users.id', ondelete='CASCADE'),
                         nullable=False
                        )
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        amenity_ids = []
        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
        reviews = relationship('Review', cascade='all, delete',
                               back_populates='place')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            from models.review import Review
            all_reviews = models.storage.all(Review)
            return [review for review in all_reviews.values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            from models.amenity import Amenity
            all_amenities = models.storage.all(Amenity)
            return [amenity for amenity in all_amenities.values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def append(self, amenity):
            if type(amenity) == Amenity:
                self.amenity_ids.append(amenity.id)
