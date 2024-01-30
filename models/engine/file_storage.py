#!/usr/bin/python3
"""FileStorage class defined."""
from models.base_model import BaseModel
from models.user import User
import json
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place

class FileStorage:
    """abstracted storage engine representation.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """dictionary __objects returned."""
        return FileStorage.__objects

    def new(self, obj):
        """__objects obj set in  with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = objct

    def save(self):
        """__objects Serialized to the JSON file __file_path."""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """JSON file __file_path deserialize to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                obdict = json.load(f)
                for o in obdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
