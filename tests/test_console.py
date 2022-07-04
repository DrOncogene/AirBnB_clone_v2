#!/usr/bin/env python3
"""unittest test file for compile.py module"""
import unittest
import os
from io import StringIO
from unittest.mock import patch
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand


class TestHelp(unittest.TestCase):
    """ tests the help command"""
    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        self.assertIn("Documented commands", f.getvalue())

    def test_help_create(self):
        """ test correct help output for create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
        create_doc = HBNBCommand().do_create.__doc__
        self.assertEqual(f.getvalue()[:-1], create_doc)

    def test_help_show(self):
        """test correct help output for show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
        show_doc = HBNBCommand().do_show.__doc__
        self.assertEqual(f.getvalue()[:-1], show_doc)

    def test_help_destroy(self):
        """ test correct help output for destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
        destroy_doc = HBNBCommand().do_destroy.__doc__
        self.assertEqual(f.getvalue()[:-1], destroy_doc)

    def test_help_all(self):
        """ test correct help output for all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
        all_doc = HBNBCommand().do_all.__doc__
        self.assertEqual(f.getvalue()[:-1], all_doc)

    def test_help_update(self):
        """ test correct help output for update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
        update_doc = HBNBCommand().do_update.__doc__
        self.assertEqual(f.getvalue()[:-1], update_doc)

    def test_help_quit(self):
        """test correct help output for quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
        quit_doc = HBNBCommand().do_quit.__doc__
        self.assertEqual(f.getvalue()[:-1], quit_doc)

    def test_help_EOF(self):
        """test correct help output for EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
        EOF_doc = HBNBCommand().do_EOF.__doc__
        self.assertEqual(f.getvalue()[:-1], EOF_doc)


class TestMiscellaneousCommands(unittest.TestCase):
    '''test EOF, quit commands and emptyline + Enter'''

    def test_empty_line_enter(self):
        """test the empty line + enter command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
        self.assertEqual(f.getvalue(), "")

    def test_quit_command(self):
        ''' test quit command'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertRaises(SystemExit, HBNBCommand().onecmd, "quit")

    def test_EOF_command(self):
        ''' test EOF command'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertRaises(SystemExit, HBNBCommand().onecmd, "EOF")


class TestCreateCommand(unittest.TestCase):
    '''test the create command'''

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_without_classname(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        expected = "** class name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_create_with_User_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
        id = f.getvalue()[:-1]
        key = "User.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_City_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
        id = f.getvalue()[:-1]
        key = "City.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_Place_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
        id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_State_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
        id = f.getvalue()[:-1]
        key = "State.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_Amenity_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity name Wifi")
        id = f.getvalue()[:-1]
        key = "Amenity.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_Review_model(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
        id = f.getvalue()[:-1]
        key = "Review.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_with_params_invalid_syntax(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place name=Oregon latitude=55\
                                  longitude=124.3')
        id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertNotEqual(storage.all()[key].name, "Oregon")
        self.assertNotEqual(storage.all()[key].latitude, 55)
        self.assertEqual(storage.all()[key].longitude, 124.3)

    def test_create_with_params_invalid_properties(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place nginx="True" size=55\
                                  color="Blue"')
        id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all())
        with self.assertRaises(AttributeError):
            storage.all()[key].nginx
            storage.all()[key].size
            storage.all()[key].color

    def test_create_User_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User first_name="John"\
                                  last_name="Doe"')
        id = f.getvalue()[:-1]
        key = "User.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].first_name, "John")
        self.assertEqual(storage.all()[key].last_name, "Doe")

    def test_create_City_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City name="New_York"')
        id = f.getvalue()[:-1]
        key = "City.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "New York")

    def test_create_Place_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place name="The_Crib" latitude=50.0\
                                  price_by_night="$50" max_guest=50')
        id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all())

    def test_create_State_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Lagos"')
        id = f.getvalue()[:-1]
        key = "State.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Lagos")

    def test_create_Amenity_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity name="Internet"')
        id = f.getvalue()[:-1]
        key = "Amenity.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Internet")

    def test_create_Review_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review text="It_was_awesome"')
        id = f.getvalue()[:-1]
        key = "Review.{}".format(id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].text, "It was awesome")


class TestShowCommand(unittest.TestCase):
    ''' test the show command '''

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_without_classname(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        expected = "** class name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 7585966")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_show_with_User(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User {}".format(id))
        key = "User.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_State(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show State {}".format(id))
        key = "State.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Place(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Place {}".format(id))
        key = "Place.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Amenity(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Amenity {}".format(id))
        key = "Amenity.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Review(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Review {}".format(id))
        key = "Review.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_without_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_show_with_invalid_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show(7585966)")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_show_with_User_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.show({})".format(id))
        key = "User.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_State_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.show({})".format(id))
        key = "State.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Place_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Place.show({})".format(id))
        key = "Place.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Amenity_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.show({})".format(id))
        key = "Amenity.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))

    def test_show_with_Review_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Review.show({})".format(id))
        key = "Review.{}".format(id)
        obj = storage.all()[key]
        self.assertEqual(f.getvalue()[:-1], str(obj))


class TestDestroyCommand(unittest.TestCase):
    '''test the destroy command'''

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_destroy_without_classname(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        expected = "** class name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel model")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_destroy_with_User(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue()[:-1]
        key = "User.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy User {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Place(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy Place {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_State(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue()[:-1]
        key = "State.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy State {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_City(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue()[:-1]
        key = "City.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy City {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Amenity(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue()[:-1]
        key = "Amenity.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy Amenity {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Review(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue()[:-1]
        key = "Review.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("destroy Review {}".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_without_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_destroy_with_invalid_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy(model)")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_destroy_with_User_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue()[:-1]
        key = "User.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("User.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Place_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue()[:-1]
        key = "Place.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("Place.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_State_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue()[:-1]
        key = "State.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("State.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_City_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue()[:-1]
        key = "City.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("City.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Amenity_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue()[:-1]
        key = "Amenity.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("Amenity.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())

    def test_destroy_with_Review_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue()[:-1]
        key = "Review.{}".format(id)
        self.assertIn(key, storage.all().keys())
        HBNBCommand().onecmd("Review.destroy({})".format(id))
        self.assertNotIn(key, storage.all().keys())


class TestAllCommand(unittest.TestCase):
    """Tests the all command"""
    @classmethod
    def setUp(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create State")
            HBNBCommand().onecmd("create City")
            HBNBCommand().onecmd("create Place")
            HBNBCommand().onecmd("create Amenity")
            HBNBCommand().onecmd("create Review")

    def test_all_without_classname(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        expected = []
        for key, obj in storage.all().items():
            expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_User(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
        expected = []
        for key, obj in storage.all().items():
            if "User" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Place(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Place")
        expected = []
        for key, obj in storage.all().items():
            if "Place" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_State(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
        expected = []
        for key, obj in storage.all().items():
            if "State" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_City(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all City")
        expected = []
        for key, obj in storage.all().items():
            if "City" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Amenity(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Amenity")
        expected = []
        for key, obj in storage.all().items():
            if "Amenity" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Review(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
        expected = []
        for key, obj in storage.all().items():
            if "Review" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_User_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.all()")
        expected = []
        for key, obj in storage.all().items():
            if "User" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Place_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Place.all()")
        expected = []
        for key, obj in storage.all().items():
            if "Place" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_State_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.all()")
        expected = []
        for key, obj in storage.all().items():
            if "State" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_City_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("City.all()")
        expected = []
        for key, obj in storage.all().items():
            if "City" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Amenity_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.all()")
        expected = []
        for key, obj in storage.all().items():
            if "Amenity" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))

    def test_all_with_Review_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
        expected = []
        for key, obj in storage.all().items():
            if "Review" in key:
                expected.append(str(obj))
        self.assertEqual(f.getvalue()[:-1], str(expected))


class TestUpdateCommand(unittest.TestCase):
    '''test the update command'''
    @classmethod
    def setUpClass(cls):
        cls.user = User()
        cls.place = Place()
        cls.state = State()
        cls.city = City()
        cls.amenity = Amenity()
        cls.review = Review()

        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

        cls.user.save()
        cls.place.save()
        cls.state.save()
        cls.city.save()
        cls.amenity.save()
        cls.review.save()

    @classmethod
    def tearDownClass(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_without_classname(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        expected = "** class name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User an_id")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_without_attr_name(self):
        id = self.user.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User {}".format(id))
        expected = "** attribute name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_without_attr_value(self):
        id = self.user.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User {} name".format(id))
        expected = "** value missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_User(self):
        id = self.user.id
        self.assertNotEqual(self.user.email, "we@alx.com")
        HBNBCommand().onecmd('update User {} email "we@alx.com"'.format(id))
        key = "User.{}".format(id)
        self.user = storage.all()[key]
        self.assertEqual(self.user.email, 'we@alx.com')

    def test_update_Place(self):
        id = self.place.id
        self.assertNotEqual(self.place.latitude, 45.5)
        HBNBCommand().onecmd('update Place {} latitude 45.5'.format(id))
        key = "Place.{}".format(id)
        self.place = storage.all()[key]
        self.assertEqual(self.place.latitude, 45.5)

    def test_update_State(self):
        id = self.state.id
        self.assertNotEqual(self.state.name, "Ibadan")
        HBNBCommand().onecmd('update State {} name "Ibadan"'.format(id))
        key = "State.{}".format(id)
        self.assertEqual(self.state.name, "Ibadan")

    def test_update_City(self):
        id = self.city.id
        self.assertNotEqual(self.city.state_id, self.state.id)
        HBNBCommand().onecmd('update City {} state_id {}'
                             .format(id, self.state.id))
        key = "City.{}".format(id)
        self.city = storage.all()[key]
        self.assertEqual(self.city.state_id, self.state.id)

    def test_update_Amenity(self):
        id = self.amenity.id
        self.assertNotEqual(self.amenity.name, "Internet")
        HBNBCommand().onecmd('update Amenity {} name Internet'.format(id))
        key = "Amenity.{}".format(id)
        self.amenity = storage.all()[key]
        self.assertEqual(self.amenity.name, "Internet")

    def test_update_Review(self):
        id = self.review.id
        self.assertNotEqual(self.review.user_id, self.user.id)
        HBNBCommand().onecmd('update Review {} user_id {}'
                             .format(id, self.user.id))
        key = "Review.{}".format(id)
        self.review = storage.all()[key]
        self.assertEqual(self.review.user_id, self.user.id)

    def test_update_without_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update()")
        expected = "** instance id missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_with_invalid_id_alternate(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update(an_id)")
        expected = "** no instance found **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_without_attr_name_alternate(self):
        id = self.base.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update({})".format(id))
        expected = "** attribute name missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_without_attr_value_alternate(self):
        id = self.user.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.update({}, name)".format(id))
        expected = "** value missing **\n"
        self.assertEqual(f.getvalue(), expected)

    def test_update_User_alternate(self):
        id = self.user.id
        self.assertNotEqual(self.user.email, "we@alx.com")
        HBNBCommand().onecmd('User.update({}, email, "we@alx.com")'
                             .format(id))
        key = "User.{}".format(id)
        self.user = storage.all()[key]
        self.assertEqual(self.user.email, 'we@alx.com')

    def test_update_Place_alternate(self):
        id = self.place.id
        self.assertNotEqual(self.place.latitude, 45.5)
        HBNBCommand().onecmd('Place.update({}, latitude, 45.5)'.format(id))
        key = "Place.{}".format(id)
        self.place = storage.all()[key]
        self.assertEqual(self.place.latitude, 45.5)

    def test_update_State_alternate(self):
        id = self.state.id
        self.assertNotEqual(self.state.name, "Ibadan")
        HBNBCommand().onecmd('State.update({}, name, "Ibadan")'.format(id))
        key = "State.{}".format(id)
        self.state = storage.all()[key]
        self.assertEqual(self.state.name, "Ibadan")

    def test_update_City_alternate(self):
        id = self.city.id
        self.assertNotEqual(self.city.state_id, self.state.id)
        HBNBCommand().onecmd('City.update({}, state_id, {})'
                             .format(id, self.state.id))
        key = "City.{}".format(id)
        self.city = storage.all()[key]
        self.assertEqual(self.city.state_id, self.state.id)

    def test_update_Amenity_alternate(self):
        id = self.amenity.id
        self.assertNotEqual(self.amenity.name, "Internet")
        HBNBCommand().onecmd('Amenity.update({}, name, Internet)'.format(id))
        key = "Amenity.{}".format(id)
        self.amenity = storage.all()[key]
        self.assertEqual(self.amenity.name, "Internet")

    def test_update_Review_alternate(self):
        id = self.review.id
        self.assertNotEqual(self.review.user_id, self.user.id)
        HBNBCommand().onecmd('Review.update({}, user_id, {})'
                             .format(id, self.user.id))
        key = "Review.{}".format(id)
        self.review = storage.all()[key]
        self.assertEqual(self.review.user_id, self.user.id)

    def test_update_User_with_dict(self):
        id = self.user.id
        self.assertNotEqual(self.user.email, "we@alx.com")
        HBNBCommand().onecmd('User.update({}, {{"email": "we@alx.com"}})'
                             .format(id))
        key = "User.{}".format(id)
        self.user = storage.all()[key]
        self.assertEqual(self.user.email, 'we@alx.com')

    def test_update_State_with_dict(self):
        id = self.state.id
        self.assertNotEqual(self.state.name, "Ibadan")
        HBNBCommand().onecmd('State.update({}, {{"name": "Ibadan"}})'
                             .format(id))
        key = "State.{}".format(id)
        self.state = storage.all()[key]
        self.assertEqual(self.state.name, "Ibadan")

    def test_update_City_with_dict(self):
        id = self.city.id
        self.assertNotEqual(self.city.state_id, self.state.id)
        HBNBCommand().onecmd('City.update({}, {{"state_id": "{}"}})'
                             .format(id, self.state.id))
        key = "City.{}".format(id)
        self.city = storage.all()[key]
        self.assertEqual(self.city.state_id, self.state.id)

    def test_update_Amenity_with_dict(self):
        id = self.amenity.id
        self.assertNotEqual(self.amenity.name, "Internet")
        HBNBCommand().onecmd('Amenity.update({}, {{"name": "Internet"}})'
                             .format(id))
        key = "Amenity.{}".format(id)
        self.amenity = storage.all()[key]
        self.assertEqual(self.amenity.name, "Internet")

    def test_update_Review_with_dict(self):
        id = self.review.id
        self.assertNotEqual(self.review.user_id, self.user.id)
        HBNBCommand().onecmd('Review.update({}, {{"user_id": "{}"}})'
                             .format(id, self.user.id))
        key = "Review.{}".format(id)
        self.review = storage.all()[key]
        self.assertEqual(self.review.user_id, self.user.id)

    def test_update_Place_with_dict(self):
        id = self.place.id
        self.assertNotEqual(self.place.city_id, self.city.id)
        self.assertNotEqual(self.place.user_id, self.user.id)
        self.assertNotEqual(self.place.longitude, 100.0)
        self.assertNotEqual(self.place.latitude, 45.5)
        city = self.city.id
        user = self.user.id
        HBNBCommand().onecmd(
                             'Place.update({}, {{\
                             "city_id":"{}",\
                             "user_id":"{}",\
                             "longitude": "100.0",\
                             "latitude": "45.5"\
                             }})'.format(id, city, user)
                            )
        key = "Place.{}".format(id)
        self.place = storage.all()[key]
        self.assertEqual(self.place.latitude, 45.5)
        self.assertEqual(self.place.longitude, 100.0)
        self.assertEqual(self.place.city_id, self.city.id)
        self.assertEqual(self.place.user_id, self.user.id)


class TestCountCommand(unittest.TestCase):
    '''test the .count() command'''
    @classmethod
    def setUpClass(cls):
        cls.user = User()
        cls.place = Place()
        cls.state = State()
        cls.city = City()
        cls.amenity = Amenity()
        cls.review = Review()

        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

        cls.user.save()
        cls.place.save()
        cls.state.save()
        cls.city.save()
        cls.amenity.save()
        cls.review.save()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_User(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is User:
                expected += 1
        self.assertEqual(count, expected)

    def test_count_Place(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Place.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is Place:
                expected += 1
        self.assertEqual(count, expected)

    def test_count_State(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is State:
                expected += 1
        self.assertEqual(count, expected)

    def test_count_City(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("City.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is City:
                expected += 1
        self.assertEqual(count, expected)

    def test_count_Amenity(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is Amenity:
                expected += 1
        self.assertEqual(count, expected)

    def test_count_Review(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Review.count()")
        count = int(f.getvalue()[:-1])
        expected = 0
        for obj in storage.all().values():
            if type(obj) is Review:
                expected += 1
        self.assertEqual(count, expected)


if __name__ == "__main__":
    unittest.main()
