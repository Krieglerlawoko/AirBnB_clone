#!/usr/bin/python3
"""tests for review.py defined

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import models
import os
import unittest
from time import sleep
from datetime import datetime
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """tests for instantiation of Review class"""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())


    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_place_id_is_public_class_attribute(self):
        riv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(riv))
        self.assertNotIn("place_id", riv.__dict__)

    def test_user_id_is_public_class_attribute(self):
        riv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(riv))
        self.assertNotIn("user_id", riv.__dict__)

    def test_text_is_public_class_attribute(self):
        riv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(riv))
        self.assertNotIn("text", riv.__dict__)

    def test_two_reviews_unique_ids(self):
        riv1 = Review()
        riv2 = Review()
        self.assertNotEqual(riv1.id, riv2.id)

    def test_two_reviews_different_created_at(self):
        riv1 = Review()
        sleep(0.05)
        riv2 = Review()
        self.assertLess(riv1.created_at, riv2.created_at)

    def test_two_reviews_different_updated_at(self):
        riv1 = Review()
        sleep(0.05)
        riv2 = Review()
        self.assertLess(riv1.updated_at, riv2.updated_at)

    def test_str_representation(self):
        dte = datetime.today()
        dte_repr = repr(dte)
        riv = Review()
        riv.id = "123456"
        riv.created_at = riv.updated_at = dte
        rivstr = riv.__str__()
        self.assertIn("[Review] (123456)", rivstr)
        self.assertIn("'id': '123456'", rivstr)
        self.assertIn("'created_at': " + dte_repr, rivstr)
        self.assertIn("'updated_at': " + dte_repr, rivstr)

    def test_args_unused(self):
        riv = Review(None)
        self.assertNotIn(None, riv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dte = datetime.today()
        dte_iso = dte.isoformat()
        riv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(riv.id, "345")
        self.assertEqual(riv.created_at, dte)
        self.assertEqual(riv.updated_at, dte)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """tests for save method of Review class."""

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
        riv = Review()
        sleep(0.05)
        first_updated_at = riv.updated_at
        riv.save()
        self.assertLess(first_updated_at, riv.updated_at)

    def test_two_saves(self):
        riv = Review()
        sleep(0.05)
        first_updated_at = riv.updated_at
        riv.save()
        second_updated_at = riv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        riv.save()
        self.assertLess(second_updated_at, riv.updated_at)

    def test_save_with_arg(self):
        riv = Review()
        with self.assertRaises(TypeError):
            riv.save(None)

    def test_save_updates_file(self):
        riv = Review()
        riv.save()
        rivid = "Review." + riv.id
        with open("file.json", "r") as f:
            self.assertIn(rivid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """tests for to_dict method of Review class"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        riv = Review()
        self.assertIn("id", riv.to_dict())
        self.assertIn("created_at", riv.to_dict())
        self.assertIn("updated_at", riv.to_dict())
        self.assertIn("__class__", riv.to_dict())

    def test_to_dict_contains_added_attributes(self):
        riv = Review()
        riv.middle_name = "Holberton"
        riv.my_number = 90
        self.assertEqual("Holberton", riv.middle_name)
        self.assertIn("my_number", riv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        riv = Review()
        riv_dict = riv.to_dict()
        self.assertEqual(str, type(riv_dict["id"]))
        self.assertEqual(str, type(riv_dict["created_at"]))
        self.assertEqual(str, type(riv_dict["updated_at"]))

    def test_to_dict_output(self):
        dte = datetime.today()
        riv = Review()
        riv.id = "123456"
        riv.created_at = riv.updated_at = dte
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dte.isoformat(),
            'updated_at': dte.isoformat(),
        }
        self.assertDictEqual(riv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        riv = Review()
        self.assertNotEqual(rv.to_dict(), riv.__dict__)

    def test_to_dict_with_arg(self):
        riv = Review()
        with self.assertRaises(TypeError):
            riv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
