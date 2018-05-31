#!/usr/bin/python3
#coding: utf-8

import os
import sys
import imp


FILE_TEMP = (
    'package %(pkg_name)s;\n\n'
    '%(imports)s\n\n\n'
    '%(pojo_body)s'
)

IMPORT_TEMP = 'import %s;'

CLASS_TEMP = (
    'public class %(name)s {\n\n'
    '%(attrs)s\n\n'
    '%(getters)s\n\n'
    '%(setters)s\n\n'
    '}'
)

ATTR_TEMP = '\tprivate %(type)s %(name)s;'

GETTER_TEMP = (
    '\tpublic %(type)s %(func_name)s() {\n'
    '\t\treturn this.%(attr_name)s;\n'
    '\t}'
)

SETTER_TEMP = (
    '\tpublic void %(func_name)s(%(type)s %(attr_name)s) {\n'
    '\t\tthis.%(attr_name)s = %(attr_name)s;\n'
    '\t}'
)


class PojoGenerator():

    '''Java POJO Generator

    examples:

        1. generate POJO from Python class:

            # Define a python class, the class name is the name of the POJO
            # class, each attribute have a string value that contains the
            # Java type.

            Class Pojo:

                attr0 = 'int'
                attr1 = 'String'
                attr2 = 'List<String>'

            generator = PojoGenerator()
            generator.gen_str_from_class(Pojo)

        2. generate POJO from Python source code:

            # You can write the Pojo class above into a file, then pass
            # the path of file to function gen_str_from_file.
            # This function will import the source code by invoking
            # imp.load_source, so the .py extension is not necessary.

            generator = PojoGenerator()
            pojos = generator.gen_str_from_file('path/to/file')
    '''

    def render_class(self, name, attrs, getters, setters):
        return CLASS_TEMP % {
            'name': name,
            'attrs': '\n'.join(attrs),
            'getters': '\n\n'.join(getters),
            'setters': '\n\n'.join(setters),
        }

    def render_attr(self, attr_type, attr_name):
        return ATTR_TEMP % {
            'type': attr_type,
            'name': attr_name,
        }

    def render_getter(self, rtype, func_name, attr_name):
        return GETTER_TEMP % {
            'type': rtype,
            'func_name': func_name,
            'attr_name': attr_name,
        }

    def render_setter(self, arg_type, func_name, attr_name):
        return SETTER_TEMP % {
            'func_name': func_name,
            'type': arg_type,
            'attr_name': attr_name,
        }

    @classmethod
    def filter(cls, obj):
        return {
            k: v for k, v in obj.__dict__.items()
            if not (k.startswith('__') and k.endswith('__'))
        }

    def attrnm_2_getternm(self, attr_name):
        func_name = attr_name.upper()[0] + attr_name[1:]
        return 'get' + func_name

    def attrnm_2_setternm(self, attr_name):
        func_name = attr_name.upper()[0] + attr_name[1:]
        return 'set' + func_name

    def gen_str_from_class(self, cls, as_file=False):
        ''' generate Java Pojo code from a python class

        :param cls: the Python class
        :param as_file: generate the Pojo code as a Java source code file
                        (with packge and import statements)
        '''

        attrs = []
        getters = []
        setters = []

        filtered_obj = self.filter(cls)
        for attr_name, attr_type in filtered_obj.items():
            attrs.append(
                self.render_attr(attr_type, attr_name)
            )

            getter_name = self.attrnm_2_getternm(attr_name)
            getters.append(
                self.render_getter(attr_type, getter_name, attr_name)
            )

            setter_name = self.attrnm_2_setternm(attr_name)
            setters.append(
                self.render_setter(attr_type, setter_name, attr_name)
            )

        class_name = cls.__name__
        pojo = self.render_class(
                   class_name,
                   attrs,
                   getters,
                   setters,
               )

        if as_file:
            imports = getattr(cls, '__imports__', [])

            import_code = '\n'.join(
                [IMPORT_TEMP % import_ for import_ in imports]
            )

            return FILE_TEMP % {
                'pkg_name': cls.__pkg__,
                'imports': import_code,
                'pojo_body': pojo,
            }
        else:
            return pojo

    def gen_str_from_file(self, file_path):
        ''' generate Pojo code from a file

        :param file_path: path to a Python source code file that contains
                          Python classes
        '''

        module = imp.load_source('pojos', file_path)
        pojo_names = self.filter(module)

        return [
            self.gen_str_from_class(getattr(module, pojo_name))
            for pojo_name in pojo_names
        ]


if __name__ == '__main__':
    vim_tempfile = sys.argv[1]
    generator = PojoGenerator()
    pojos = generator.gen_str_from_file(vim_tempfile)
    pojo_code = '\n\n\n'.join(pojos)

    with open(vim_tempfile, 'w') as f:
        f.write(pojo_code)
