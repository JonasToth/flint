#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test if the implicit none check does catch everything he promises.
"""

import logging
from os.path import dirname, join
import re
import unittest
from file_io import CodeFile
from check.check_implicit_none import _match_implicit, CheckImplicitNone

# logging.basicConfig(level=logging.DEBUG)


class TestCheckImplicitNone(unittest.TestCase):
    """Test if the check works on all code constructs as expected."""

    def test_regex_implicit(self):
        self.assertTrue(_match_implicit("implicit none"))
        self.assertTrue(_match_implicit("implicit   none"))
        self.assertTrue(_match_implicit("implicit \tnone"))
        self.assertTrue(_match_implicit("implicit \t none"))
        self.assertTrue(_match_implicit("implicit none"))
        self.assertTrue(_match_implicit(" implicit none"))
        self.assertTrue(_match_implicit("\t implicit none"))
        self.assertTrue(_match_implicit("\t implicit none  ! alsd"))
        self.assertTrue(_match_implicit("\t implicit none  "))
        self.assertTrue(_match_implicit("implicit none  "))
        self.assertTrue(_match_implicit("implicit none \t "))

        self.assertFalse(_match_implicit("! implicit none \t "))
        self.assertFalse(_match_implicit("!implicit none \t "))
        self.assertFalse(_match_implicit("   !   implicit none"))
        self.assertFalse(_match_implicit(" \t ! \t implicit none"))
        self.assertFalse(_match_implicit(" \t ! \timplicit none "))
        self.assertFalse(_match_implicit(" \t ! \t implicit none ! laksd"))
        self.assertFalse(_match_implicit(" \t ! \t implicit none !\tlaksd"))
        self.assertFalse(_match_implicit(" \t !\t implicit none!\tlaksd"))
        self.assertFalse(_match_implicit(" \t ! \t implicit none\t"))

    def test_simple(self):
        f_file = CodeFile(
            join(dirname(__file__), "../../test/check/implicit_none_simple.f90"))
        c = CheckImplicitNone(f_file)
        c.check()

        self.assertListEqual([16, 18, 22, 32], sorted(c._occurences))

    def test_edgecase(self):
        f_file = CodeFile(
            join(dirname(__file__), "../../test/check/implicit_none_edge.f90"))
        c = CheckImplicitNone(f_file)
        c.check()

        self.assertListEqual([1, 4, 7], sorted(c._occurences))

    def test_real_world(self):
        f_file = CodeFile(
            join(dirname(__file__), "../../test/check/implicit_none_real.f90"))
        c = CheckImplicitNone(f_file)
        c.check()

        self.assertListEqual([43,51], sorted(c._occurences))
