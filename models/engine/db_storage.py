#!/usr/bin/python3
""" module that defines the db storage engine"""
import os
import MySQLdb as sqldb
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """ the db storage class"""
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f"mysql://{user}:{passwd}\
                                      @{host}:3306/{db_name}",
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            db = sqldb.connect(host=host, port=3306, user=user,
                               passwd=passwd, db=db_name)
            c = db.cursor()
            script_name = os.path.join(os.path.dirname(__file__),
                                       'drop_all_tables.sql')
            f = open(script_name, 'r')
            c.execute(f.read())

    def all(self, cls=None):
        """ queries the db for all objects"""
        models = import_models()
        session = self.__session
        obj_list = []
        obj_dict = {}
        if cls is None:
            for key, value in models.items():
                if key != 'BaseModel' and key != 'Base':
                    obj_list.extend(session.query(value).all())
            for obj in obj_list:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict.update({key: obj})
            return obj_dict
        for key, value in models.items():
            if value == cls:
                obj_list.extend(session.query(models[key]).all())
        for obj in obj_list:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict.update({key: obj})

        return obj_dict

    def new(self, obj):
        """ adds a new obj to the db session"""
        self.__session.add(obj)

    def save(self):
        """ commits all changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes obj from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ creates all db tables"""
        models = import_models()
        Base = models['Base']
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()


def import_models():
    from models.base_model import BaseModel, Base
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review
    models = {
        "BaseModel": BaseModel,
        "Base": Base,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }
    return models
