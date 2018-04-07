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
            "PROGRAM test_program\n",
            "  integer  :: zahl ! Wir definieren eine Zahl\n",
            "END PROGRAM test_program\n",
        ]
        insensitive_content = [
            "program test_program\n",
            "  integer  :: zahl ! wir definieren eine zahl\n",
            "end program test_program\n",
        ]

        print(f_file.insensitive_lines())

        self.assertListEqual(original_content, f_file.original_lines())
        self.assertListEqual(insensitive_content, f_file.insensitive_lines())


if __name__ == "__main__":
    unittest.main()
