#!/usr/bin/python3
"""Tests for models/amenity.py defined.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""

import models
import unittest
import os
from time import sleep
from datetime import datetime
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Tests for instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amty = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amty.__dict__)

    def test_two_amenities_unique_ids(self):
        amty1 = Amenity()
        amty2 = Amenity()
        self.assertNotEqual(amty1.id, amty2.id)

    def test_two_amenities_different_created_at(self):
        amty1 = Amenity()
        sleep(0.05)
        amty2 = Amenity()
        self.assertLess(amty1.created_at, amty2.created_at)

    def test_two_amenities_different_updated_at(self):
        amty1 = Amenity()
        sleep(0.05)
        amty2 = Amenity()
        self.assertLess(amty1.updated_at, amty2.updated_at)

    def test_str_representation(self):
        dte = datetime.today()
        dte_repr = repr(dte)
        amty = Amenity()
        amty.id = "123456"
        amty.created_at = amty.updated_at = dte
        amtystr = amty.__str__()
        self.assertIn("[Amenity] (123456)", amtystr)
        self.assertIn("'id': '123456'", amtystr)
        self.assertIn("'created_at': " + dt_repr, amtystr)
        self.assertIn("'updated_at': " + dt_repr, amtystr)

    def test_args_unused(self):
        amty = Amenity(None)
        self.assertNotIn(None, amty.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation using kwargs test method"""
        dte = datetime.today()
        dte_iso = dte.isoformat()
        amty = Amenity(id="345", created_at=dte_iso, updated_at=dte_iso)
        self.assertEqual(amty.id, "345")
        self.assertEqual(amty.created_at, dte)
        self.assertEqual(amty.updated_at, dte)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Tests for testing save method of the Amenity class."""

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
        amty = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        amty.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        amty = Amenity()
        sleep(0.05)
        first_updated_at = amty.updated_at
        amty.save()
        second_updated_at = amty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amty.save()
        self.assertLess(second_updated_at, amty.updated_at)

    def test_save_with_arg(self):
        amty = Amenity()
        with self.assertRaises(TypeError):
            amty.save(None)

    def test_save_updates_file(self):
        amty = Amenity()
        amty.save()
        amtyid = "Amenity." + amty.id
        with open("file.json", "r") as f:
            self.assertIn(amtyid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Tests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amty = Amenity()
        self.assertIn("id", amty.to_dict())
        self.assertIn("created_at", amty.to_dict())
        self.assertIn("updated_at", amty.to_dict())
        self.assertIn("__class__", amty.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amty = Amenity()
        amty.middle_name = "Holberton"
        amty.my_number = 98
        self.assertEqual("Holberton", amty.middle_name)
        self.assertIn("my_number", amty.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amty = Amenity()
        amty_dict = amty.to_dict()
        self.assertEqual(str, type(amty_dict["id"]))
        self.assertEqual(str, type(amty_dict["created_at"]))
        self.assertEqual(str, type(amty_dict["updated_at"]))

    def test_to_dict_output(self):
        dte = datetime.today()
        amty = Amenity()
        amty.id = "123456"
        amty.created_at = amty.updated_at = dte
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dte.isoformat(),
            'updated_at': dte.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amty = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(self):
        amty = Amenity()
        with self.assertRaises(TypeError):
            amty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
