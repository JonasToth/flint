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
from check.check_implicit_none import _match_implicit, _match_start_construct,\
                                      _match_end_construct, CheckImplicitNone

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

    def test_regex_start_construct(self):
        self.assertTrue(_match_start_construct("function my_function"))
        self.assertTrue(_match_start_construct("  function alksjd"))
        self.assertTrue(_match_start_construct("\tfunction ! bla "))
        self.assertTrue(_match_start_construct(" \t function asdj  "))

        self.assertFalse(_match_start_construct("!function"))
        self.assertFalse(_match_start_construct("!  end   function"))
        self.assertFalse(_match_start_construct("\t! \tfunction ! bla "))
        self.assertFalse(_match_start_construct(" \t ! \t function ! kajlsd"))
        self.assertFalse(_match_start_construct(" \t ! function commentary"))

        self.assertTrue(_match_start_construct("\tsubroutine"))
        self.assertTrue(_match_start_construct("\t subroutine"))
        self.assertTrue(_match_start_construct("\tsubroutine"))
        self.assertTrue(_match_start_construct("\t subroutine"))

        self.assertTrue(_match_start_construct("program"))
        self.assertTrue(_match_start_construct("program"))
        self.assertTrue(_match_start_construct("\tprogram"))
        self.assertTrue(_match_start_construct("\t program"))

    def test_regex_end_construct(self):
        self.assertTrue(_match_end_construct("end function"))
        self.assertTrue(_match_end_construct("  end   function"))
        self.assertTrue(_match_end_construct("end\tfunction ! bla "))
        self.assertTrue(_match_end_construct("end \t function"))

        self.assertFalse(_match_end_construct("!end function"))
        self.assertFalse(_match_end_construct("!  end   function"))
        self.assertFalse(_match_end_construct("\t! end\tfunction ! bla "))
        self.assertFalse(
            _match_end_construct(" \t ! end \t function ! kajlsd"))

        self.assertTrue(_match_end_construct("\tend subroutine"))
        self.assertTrue(_match_end_construct("\t end   subroutine"))
        self.assertTrue(_match_end_construct("end\tsubroutine"))
        self.assertTrue(_match_end_construct("end \t subroutine"))

        self.assertTrue(_match_end_construct("end program"))
        self.assertTrue(_match_end_construct("end   program"))
        self.assertTrue(_match_end_construct("end\tprogram"))
        self.assertTrue(_match_end_construct("end \t program"))

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
