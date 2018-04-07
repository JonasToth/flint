#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test functions for common matcher functions.
"""

import unittest

from common_matcher import match_begin_block, match_end_block,\
                           match_blank_line, match_commented_line


class TestCheckCommonMatcher(unittest.TestCase):
    """Check if the common matchers match what they are supposed to match."""

    def test_match_begin_block(self):
        self.assertTrue(match_begin_block("function my_function"))
        self.assertTrue(match_begin_block("  function alksjd"))
        self.assertTrue(match_begin_block("\tfunction ! bla "))
        self.assertTrue(match_begin_block(" \t function asdj  "))

        self.assertFalse(match_begin_block("!function"))
        self.assertFalse(match_begin_block("!  end   function"))
        self.assertFalse(match_begin_block("\t! \tfunction ! bla "))
        self.assertFalse(match_begin_block(" \t ! \t function ! kajlsd"))
        self.assertFalse(match_begin_block(" \t ! function commentary"))

        self.assertTrue(match_begin_block("\tsubroutine"))
        self.assertTrue(match_begin_block("\t subroutine"))
        self.assertTrue(match_begin_block("\tsubroutine"))
        self.assertTrue(match_begin_block("\t subroutine"))

        self.assertTrue(match_begin_block("program"))
        self.assertTrue(match_begin_block("program"))
        self.assertTrue(match_begin_block("\tprogram"))
        self.assertTrue(match_begin_block("\t program"))

    def test_match_end_block(self):
        self.assertTrue(match_end_block("end function"))
        self.assertTrue(match_end_block("  end   function"))
        self.assertTrue(match_end_block("end\tfunction ! bla "))
        self.assertTrue(match_end_block("end \t function"))

        self.assertFalse(match_end_block("!end function"))
        self.assertFalse(match_end_block("!  end   function"))
        self.assertFalse(match_end_block("\t! end\tfunction ! bla "))
        self.assertFalse(match_end_block(" \t ! end \t function ! kajlsd"))

        self.assertTrue(match_end_block("\tend subroutine"))
        self.assertTrue(match_end_block("\t end   subroutine"))
        self.assertTrue(match_end_block("end\tsubroutine"))
        self.assertTrue(match_end_block("end \t subroutine"))

        self.assertTrue(match_end_block("end program"))
        self.assertTrue(match_end_block("end   program"))
        self.assertTrue(match_end_block("end\tprogram"))
        self.assertTrue(match_end_block("end \t program"))

    def test_blank_line(self):
        self.assertTrue(match_blank_line("\n"))
        self.assertTrue(match_blank_line("\t"))
        self.assertTrue(match_blank_line("   "))
        self.assertTrue(match_blank_line(" \t "))
        self.assertTrue(match_blank_line(" \t \n"))

        self.assertFalse(match_blank_line("   ! comment"))
        self.assertFalse(match_blank_line(" \t ! comment"))
        self.assertFalse(match_blank_line(" \t do i=1,10"))

    def test_commented_line(self):
        self.assertTrue(match_commented_line("! hallo"))
        self.assertTrue(match_commented_line("  ! comment"))
        self.assertTrue(match_commented_line(" \t ! comment "))
        self.assertTrue(match_commented_line(" \t!comment"))
        self.assertTrue(match_commented_line("\t!comment\n"))
        self.assertTrue(match_commented_line("!comment !comment"))
        self.assertTrue(match_commented_line("  !comment !comment"))

        self.assertFalse(match_commented_line(" something  ! comment"))
        self.assertFalse(match_commented_line(" \t do i=1,100 ! comment"))
        self.assertFalse(match_commented_line(" \t do i=1,100"))
        self.assertFalse(match_commented_line("do i=1,100"))
        self.assertFalse(match_commented_line("integer(8) i"))
        self.assertFalse(match_commented_line("integer(8) :: i"))
        self.assertFalse(match_commented_line("integer(8) :: i ! comment"))
        self.assertFalse(match_commented_line(" \t integer(8) :: i ! comment"))
