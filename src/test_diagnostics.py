#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for the diagnostic engine.
"""

from os.path import dirname, join
import unittest
from file_io import CodeFile
from diagnostics import _check_location, _create_message


class TestWarnings(unittest.TestCase):
    """Test emitting warnings."""

    def setUp(self):
        self.f_file = CodeFile(
            join(dirname(__file__), "../test/simplest_fortran_file.f90"))

    def test_check_location(self):
        self.assertRaises(AssertionError, _check_location, self.f_file, -1)
        self.assertRaises(AssertionError, _check_location, self.f_file, 10)

    def test_create_message(self):
        res = "{}: 2: note: defining variable here".format(self.f_file.path())
        self.assertEqual(res,
                         _create_message(self.f_file, 2, "note",
                                         "defining variable here"))


if __name__ == "__main__":
    unittest.main()
