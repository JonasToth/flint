#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for `CodeFile`
"""

from os.path import dirname, join
import unittest
from file_io import CodeFile


class TestCodeFile(unittest.TestCase):
    """Test functions for `CodeFile`."""

    def test_file_path(self):
        f_file = CodeFile("mod_functions.f90")
        self.assertTrue(f_file.path().startswith('/'))

    def test_read_in(self):
        f_file = CodeFile(
            join(dirname(__file__), "../test/simplest_fortran_file.f90"))

        original_content = [
            "PROGRAM test_program",
            "  integer  :: zahl ! Wir definieren eine Zahl",
            "END PROGRAM test_program",
        ]
        insensitive_content = [
            "program test_program",
            "  integer  :: zahl ! wir definieren eine zahl",
            "end program test_program",
        ]

        for (i, line) in enumerate(f_file.original_lines()):
            self.assertEqual(line, original_content[i])

        for (i, line) in enumerate(f_file.insensitive_lines()):
            self.assertEqual(line, insensitive_content[i])


if __name__ == "__main__":
    unittest.main()
