#!/usr/bin/python3
"""Defines the HBnB console."""
import re
from models import storage
import cmd
from models.state import State
from models.user import User
from models.city import City
from models.base_model import BaseModel
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from shlex import split

def parse(arg):
    brkts = re.search(r"\[(.*?)\]", arg)
    crlBraces = re.search(r"\{(.*?)\}", arg)
    if crlBraces is None:
        if brkts is None:
            return [a.strip(",") for a in split(arg)]
        else:
            lexer = split(arg[:brkts.span()[0]])
            retl = [a.strip(",") for a in lexer]
            retl.append(brkts.group())
            return retl
    else:
        lexer = split(arg[:crlBraces.span()[0]])
        retl = [a.strip(",") for i in lexer]
        retl.append(crlBraces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Holberton AnB command interpreter defined"""

    prmpt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing if empty line"""
        pass

    def default(self, arg):
        """Default behavior for invalid input"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        mtch = re.search(r"\.", arg)
        if mtch is not None:
            argl = [arg[:mtch.span()[0]], arg[mtch.span()[1]:]]
            mtch = re.search(r"\((.*?)\)", argl[1])
            if mtch is not None:
                command = [argl[1][:mtch.span()[0]], mtch.group()[1:-1]]
                if command[0] in argdict.keys():
                    cll = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](cll)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Command to quit program"""
        return True

    def do_EOF(self, arg):
        """EOF signal exits program"""
        print("")
        return True

    def do_create(self, arg):
        """Create new instance of class and print its id"""
        agl = parse(arg)
        if len(agl) == 0:
            print("** class name missing **")
        elif agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(agl[0])().id)
            storage.save()

    def do_destroy(self, arg):
        """class instance of a given id is deleted"""
        agl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(agl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(agl[0], agl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(agl[0], agl[1])]
            storage.save()

    def do_show(self, arg):
        """Display class instance string representation of a given id"""
        agl = parse(arg)
        objdict = storage.all()
        if len(agl) == 0:
            print("** class name missing **")
        elif agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(agl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(agl[0], agl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], agl[1])])

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Update a class instance of a given id with
        a given attribute key/value pair or dictionary"""
        argxl = parse(arg)
        objdict = storage.all()

        if len(argxl) == 0:
            print("** class name missing **")
            return False
        if argxl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argxl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argxl[0], argxl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argxl) == 2:
            print("** attribute name missing **")
            return False
        if len(argxl) == 3:
            try:
                type(eval(argxl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argxl) == 4:
            obj = objdict["{}.{}".format(argxl[0], argxl[1])]
            if argxl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argxl[2]])
                obj.__dict__[argxl[2]] = valtype(argxl[3])
            else:
                obj.__dict__[argxl[2]] = argxl[3]
        elif type(eval(argxl[2])) == dict:
            obj = objdict["{}.{}".format(argxl[0], argxl[1])]
            for k, v in eval(argxl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    vltyp = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = vltyp(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
