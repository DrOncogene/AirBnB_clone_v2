#!/usr/bin/python3
""" module that defines the db storage engine"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ the db storage class"""
    __engine = None
    __session = None
    _classes = {
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(user, passwd, host, db),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ queries the db for all objects"""
        session = self.__session()
        obj_list = []
        obj_dict = {}
        if cls is None:
            for value in self._classes.values():
                obj_list.extend(session.query(value).all())
            for obj in obj_list:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict.update({key: obj})
            return obj_dict
        for key, value in self._classes.items():
            if value == cls:
                obj_list.extend(session.query(value).all())
                break
        for obj in obj_list:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict.update({key: obj})

        return obj_dict

    def new(self, obj):
        """ adds a new obj to the db session"""
        session = self.__session()
        session.add(obj)

    def save(self):
        """ commits all changes to db"""
        session = self.__session()
        session.commit()

    def delete(self, obj=None):
        """ deletes obj from the current session"""
        if obj is not None:
            session = self.__session()
            session.delete(obj)

    def reload(self):
        """ creates all db tables"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """ calls the reload method"""
        self.__session.remove()
        self.__session()
