#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for `CodeFile`
"""

import unittest
from file_io import CodeFile


class TestCodeFile(unittest.TestCase):
    """Test functions for `CodeFile`."""

    def test_file_path(self):
        f_file = CodeFile("mod_functions.f90")
        self.assertTrue(f_file.path().startswith('/'))
        
