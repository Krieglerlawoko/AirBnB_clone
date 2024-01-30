#!/usr/bin/python3
"""Tests for models/base_model.py defined.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from time import sleep


class TestBaseModel_instantiation(unittest.TestCase):
    """Tests for instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bmod1 = BaseModel()
        bmod2 = BaseModel()
        self.assertNotEqual(bmod1.id, bmod2.id)

    def test_two_models_different_created_at(self):
        bmod1 = BaseModel()
        sleep(0.05)
        bmod2 = BaseModel()
        self.assertLess(bmod1.created_at, bmod2.created_at)

    def test_two_models_different_updated_at(self):
        bmod1 = BaseModel()
        sleep(0.05)
        bmod2 = BaseModel()
        self.assertLess(bmod1.updated_at, bmod2.updated_at)

    def test_str_representation(self):
        dte = datetime.today()
        dte_repr = repr(dt)
        bmod = BaseModel()
        bmod.id = "123456"
        bmod.created_at = bmod.updated_at = dt
        bmodstr = bmod.__str__()
        self.assertIn("[BaseModel] (123456)", bmodstr)
        self.assertIn("'id': '123456'", bmodstr)
        self.assertIn("'created_at': " + dte_repr, bmodstr)
        self.assertIn("'updated_at': " + dte_repr, bmodstr)

    def test_args_unused(self):
        bmod = BaseModel(None)
        self.assertNotIn(None, bmod.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dte = datetime.today()
        dte_iso = dte.isoformat()
        bmod = BaseModel(id="345", created_at=dte_iso, updated_at=dte_iso)
        self.assertEqual(bmod.id, "345")
        self.assertEqual(bmod.created_at, dte)
        self.assertEqual(bmod.updated_at, dte)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dte = datetime.today()
        dte_iso = dte.isoformat()
        bmod = BaseModel("12", id="345", created_at=dte_iso, updated_at=dte_iso)
        self.assertEqual(bmod.id, "345")
        self.assertEqual(bmod.created_at, dt)
        self.assertEqual(bmod.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Tests for save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        bmod = BaseModel()
        sleep(0.05)
        first_updated_at = bmod.updated_at
        bmod.save()
        self.assertLess(first_updated_at, bmod.updated_at)

    def test_two_saves(self):
        bmod = BaseModel()
        sleep(0.05)
        first_updated_at = bmod.updated_at
        bmod.save()
        second_updated_at = bmod.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bmod.save()
        self.assertLess(second_updated_at, bmod.updated_at)

    def test_save_with_arg(self):
        bmod = BaseModel()
        with self.assertRaises(TypeError):
            bmod.save(None)

    def test_save_updates_file(self):
        bmod = BaseModel()
        bmod.save()
        bmodid = "BaseModel." + bmod.id
        with open("file.json", "r") as f:
            self.assertIn(bmodid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Tests for to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        bmod = BaseModel()
        self.assertTrue(dict, type(bmod.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bmod = BaseModel()
        self.assertIn("id", bmod.to_dict())
        self.assertIn("created_at", bmod.to_dict())
        self.assertIn("updated_at", bmod.to_dict())
        self.assertIn("__class__", bmod.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bmod = BaseModel()
        bmod.name = "Holberton"
        bmod.my_number = 98
        self.assertIn("name", bmod.to_dict())
        self.assertIn("my_number", bmod.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bmod = BaseModel()
        bmod_dict = bmod.to_dict()
        self.assertEqual(str, type(bmod_dict["created_at"]))
        self.assertEqual(str, type(bmod_dict["updated_at"]))

    def test_to_dict_output(self):
        dte = datetime.today()
        bmod = BaseModel()
        bmod.id = "123456"
        bmod.created_at = bmod.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dte.isoformat(),
            'updated_at': dte.isoformat()
        }
        self.assertDictEqual(bmod.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bmod = BaseModel()
        self.assertNotEqual(bmod.to_dict(), bmod.__dict__)

    def test_to_dict_with_arg(self):
        bmod = BaseModel()
        with self.assertRaises(TypeError):
            bmod.to_dict(None)


if __name__ == "__main__":
    unittest.main()
