#!/usr/bin/python3
"""Unittests for models user defined"""
import models
import unittest
import os
from time import sleep
from datetime import datetime
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests tests instantiation of the class user"""

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def test_two_users_different_created_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def test_two_users_different_updated_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_str_representation(self):
        dte = datetime.today()
        dte_repr = repr(dt)
        usr = User()
        usr.id = "123456"
        usr.created_at = us.updated_at = dte
        usstr = usr.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_args_unused(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dte = datetime.today()
        dte_iso = dte.isoformat()
        usr = User(id="345", created_at=dte_iso, updated_at=dte_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

class TestUser_save(unittest.TestCase):
    """tests for save method of the  class."""

    @classmethod
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

    def test_one_save(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_two_saves(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        second_updated_at = usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(second_updated_at, usr.updated_at)

    def test_save_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_save_updates_file(self):
        usr = User()
        usr.save()
        usid = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """test for to_dict method of the User class."""

    def test_to_dict_contains_correct_keys(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_added_attributes(self):
        usr = User()
        usr.middle_name = "Holberton"
        usr.my_number = 90
        self.assertEqual("Holberton", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def test_to_dict_output(self):
        dte = datetime.today()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = dte
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dte.isoformat(),
            'updated_at': dte.isoformat(),

    def test_contrast_to_dict_dunder_dict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_to_dict_datetime_attributes_are_strs(self):
        usr = User()
        usr_dict = usr.to_dict()
        self.assertEqual(str, type(usr_dict["id"]))
        self.assertEqual(str, type(usr_dict["created_at"]))
        self.assertEqual(str, type(usr_dict["updated_at"]))

        }
        self.assertDictEqual(us.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
