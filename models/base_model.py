#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from models import storage


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column('id', String(60), primary_key=True, nullable=False)
    created_at = Column('created_at', Date,
                        default=datetime.utcnow(), nullable=False)
    updated_at = Column('updated_at', Date,
                        default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            try:
                del kwargs['__class__']
            except KeyError:
                pass
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        obj_dict = self.to_dict()
        del obj_dict['__class__']
        return f"[{self.__class__.__name__}] ({self.id}) {obj_dict}"

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        try:
            del dictionary['_sa_instance_state']
        except KeyError:
            pass

        return dictionary

    def delete(self):
        """ delete current object from storage"""
        storage.delete(self)
