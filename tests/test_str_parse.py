import collections
from unittest import TestCase

from opylib.str_parse import (dsv_line_to_list, get_attr_multi_level,
                              str_to_class, strs_to_classes)


class Test(TestCase):
    def test_getattr_multi_level(self):
        class MyClass:
            class Sub1:
                class Sub2:
                    address = 'attribute value'

        self.assertEqual(get_attr_multi_level(MyClass, 'Sub1.Sub2.address'),
                         MyClass.Sub1.Sub2.address)

    def test_str_to_class(self):
        self.assertEqual(str_to_class('collections.Counter'),
                         collections.Counter)

    def test_strs_to_classes(self):
        exp = [collections.Counter, collections.OrderedDict,
               collections.UserDict]
        act = strs_to_classes(['collections.Counter', 'collections.OrderedDict',
                               'collections.UserDict'])
        self.assertEqual(act, exp)

    def test_dsv_line_to_list(self):
        self.assertEqual(dsv_line_to_list('a,b,c'), ['a', 'b', 'c'])
        self.assertEqual(dsv_line_to_list('a,b,c,'), ['a', 'b', 'c', ''])
        self.assertEqual(dsv_line_to_list('a,,c'), ['a', '', 'c'])
        self.assertEqual(dsv_line_to_list('a,"b",c'), ['a', 'b', 'c'])
        self.assertEqual(dsv_line_to_list('a,"b,e",c'), ['a', 'b,e', 'c'])
        self.assertEqual(dsv_line_to_list('a,"b,e"more",c'),
                         ['a', 'b,e"more', 'c'])
