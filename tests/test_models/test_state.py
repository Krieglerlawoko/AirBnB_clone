#!/usr/bin/python3
"""unittests for state.py defined

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import unittest
import models
import os
from time import sleep
from datetime import datetime
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """test for instantiation of the State class."""

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))


    def test_name_is_public_class_attribute(self):
        ste = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(ste))
        self.assertNotIn("name", ste.__dict__)

    def test_two_states_unique_ids(self):
        ste1 = State()
        ste2 = State()
        self.assertNotEqual(ste1.id, ste2.id)

    def test_two_states_different_created_at(self):
        ste1 = State()
        sleep(0.05)
        ste2 = State()
        self.assertLess(ste1.created_at, ste2.created_at)

    def test_two_states_different_updated_at(self):
        ste1 = State()
        sleep(0.05)
        ste2 = State()
        self.assertLess(ste1.updated_at, ste2.updated_at)

   def test_args_unused(self):
        ste = State(None)
        self.assertNotIn(None, ste.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dte = datetime.today()
        dte_iso = dte.isoformat()
        ste = State(id="345", created_at=dte_iso, updated_at=dte_iso)
        self.assertEqual(ste.id, "345")
        self.assertEqual(ste.created_at, dte)
        self.assertEqual(ste.updated_at, dte)

    def test_str_representation(self):
        dte = datetime.today()
        dte_repr = repr(dte)
        ste = State()
        ste.id = "123456"
        ste.created_at = ste.updated_at = dte
        ststr = ste.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dte_repr, ststr)
        self.assertIn("'updated_at': " + dte_repr, ststr)
 
    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """test for save method of the State class"""

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
        ste = State()
        sleep(0.05)
        first_updated_at = ste.updated_at
        ste.save()
        self.assertLess(first_updated_at, ste.updated_at)

    def test_two_saves(self):
        ste = State()
        sleep(0.05)
        first_updated_at = ste.updated_at
        ste.save()
        second_updated_at = ste.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ste.save()
        self.assertLess(second_updated_at, ste.updated_at)

    def test_save_with_arg(self):
        ste = State()
        with self.assertRaises(TypeError):
            ste.save(None)

    def test_save_updates_file(self):
        ste = State()
        ste.save()
        steid = "State." + ste.id
        with open("file.json", "r") as f:
            self.assertIn(steid, f.read())


class TestState_to_dict(unittest.TestCase):
    """test for to_dict method of the State class"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ste = State()
        self.assertIn("id", ste.to_dict())
        self.assertIn("created_at", ste.to_dict())
        self.assertIn("updated_at", ste.to_dict())
        self.assertIn("__class__", ste.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ste = State()
        ste.middle_name = "Holberton"
        ste.my_number = 90
        self.assertEqual("Holberton", st.middle_name)
        self.assertIn("my_number", st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ste = State()
        ste_dict = ste.to_dict()
        self.assertEqual(str, type(ste_dict["id"]))
        self.assertEqual(str, type(ste_dict["created_at"]))
        self.assertEqual(str, type(ste_dict["updated_at"]))

    def test_to_dict_output(self):
        dte = datetime.today()
        ste = State()
        ste.id = "123456"
        ste.created_at = ste.updated_at = dte
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dte.isoformat(),
            'updated_at': dte.isoformat(),
        }
        self.assertDictEqual(ste.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ste = State()
        self.assertNotEqual(ste.to_dict(), ste.__dict__)

    def test_to_dict_with_arg(self):
        ste = State()
        with self.assertRaises(TypeError):
            ste.to_dict(None)


if __name__ == "__main__":
    unittest.main()
