#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '

    _classes = {
               'BaseModel': BaseModel,
               'User': User,
               'Place': Place,
               'State': State,
               'City': City,
               'Amenity': Amenity,
               'Review': Review
              }
    _dot_cmds = ['all', 'count', 'show', 'destroy', 'update', 'create']
    _types = {
             'number_rooms': int,
             'number_bathrooms': int,
             'max_guest': int,
             'price_by_night': int,
             'latitude': float,
             'longitude': float
            }

    def default(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating i.e. 'cmd.class(args/kwargs)'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # duplicate line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand._dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])
            self.onecmd(line)

        except Exception as mess:
            super().default(line)

    def do_quit(self, command):
        """ Exits the program with formatting\n"""
        exit()

    def do_EOF(self, arg):
        """ Exits the program without formatting
        [Usage]: EOF\n"""
        print()
        exit()

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class
        [Usage]: create <className>\n"""
        if not args:
            print("** class name missing **")
            return
        args = args.split(' ')
        cls = args[0]
        params = check_params(args[1:])
        if cls not in HBNBCommand._classes:
            print("** class doesn't exist **")
            return
        new = HBNBCommand._classes[cls]()
        for param in params:
            attr, value = param.split('=')
            if attr in dir(new):
                attr_t = self._types[attr] if attr in self._types else None
                new.__dict__[attr] = (value if attr_t is None
                                      else attr_t(value))
        storage.save()
        print(new.id)

    def do_show(self, args):
        """ Method to show an individual object
        [Usage]: show <className> <objectId>\n"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand._classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroys a specified object
        [Usage]: destroy <className> <objectId>\n"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand._classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class
        [Usage]: all [<className>]\n"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand._classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def do_count(self, args):
        """Count current number of class instances
        [Usage]: count <class_name>\n"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def do_update(self, args):
        """ Updates a certain object with new info
        Usage: update <className> <id> <attName> <attVal>\n"""
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand._classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve current object from storage
        obj = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand._types:
                    att_val = HBNBCommand._types[att_name](att_val)

                # update dictionary with name, value pair
                obj.__dict__.update({att_name: att_val})

        obj.save()  # save updates to file


def check_params(params: list) -> list:
    """checks the formats of all the passed parameters and
    return a list of all valid ones"""

    valid = []
    for param in params:
        param_type = str
        is_valid = 1
        name, value = None, None
        try:
            name, value = param.split('=')
        except ValueError:
            pass

        if not value:  # if no value passed, skip
            continue

        try:
            param_type = HBNBCommand._types[name]
        except KeyError:
            pass

        if param_type == float:
            match = re.search(r'\d+\.\d+', value)
            # if float format (<unit>.<decimal>) is not found, skip
            if not match or (match and match.group() != value):
                continue
        elif param_type == int:
            match = re.search(r'\d+', value)
            # if integer format (<digits>) is not found, skip
            if not match or (match and match.group() != value):
                continue
        else:  # check string ("<str>") format
            if value[0] != '"' or value[-1] != '"':  # str not quoted, skip
                continue
            value = value.strip('"').replace('_', ' ')
            # find all double quotes to check if they are escaped
            quotes_idx = [i for i, v in enumerate(value) if v == '"']
            for idx in quotes_idx:
                try:
                    if value[idx - 1] != '\\':
                        is_valid = 0
                        break
                except IndexError:
                    is_valid = 0
                    break
        if is_valid:
            valid.append("{}={}".format(name, value.replace('\\', '')))

    return valid


if __name__ == "__main__":
    HBNBCommand().cmdloop()
