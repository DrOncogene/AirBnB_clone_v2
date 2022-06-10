#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBasemodel
from models.user import User


class TestUser(TestBasemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """test if first name is correct"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """tests the last name"""
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """tests email"""
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """tests the password"""
        new = self.value()
        self.assertEqual(type(new.password), str)
