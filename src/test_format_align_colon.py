#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test if all functions to align the double colon on subsequent lines do
work as expected.
"""

import logging
import unittest

from format_align_colon import _match_blank_line, _match_comment_line,\
                               _match_variable_colon

# logging.basicConfig(level=logging.DEBUG)


class TestFormatAlignColor(unittest.TestCase):
    def test_blank_line(self):
        self.assertTrue(_match_blank_line("\n"))
        self.assertTrue(_match_blank_line("\t"))
        self.assertTrue(_match_blank_line("   "))
        self.assertTrue(_match_blank_line(" \t "))
        self.assertTrue(_match_blank_line(" \t \n"))

        self.assertFalse(_match_blank_line("   ! comment"))
        self.assertFalse(_match_blank_line(" \t ! comment"))
        self.assertFalse(_match_blank_line(" \t do i=1,10"))

    def test_comment_line(self):
        self.assertTrue(_match_comment_line("! hallo"))
        self.assertTrue(_match_comment_line("  ! comment"))
        self.assertTrue(_match_comment_line(" \t ! comment "))
        self.assertTrue(_match_comment_line(" \t!comment"))
        self.assertTrue(_match_comment_line("\t!comment\n"))
        self.assertTrue(_match_comment_line("!comment !comment"))
        self.assertTrue(_match_comment_line("  !comment !comment"))

        self.assertFalse(_match_comment_line(" something  ! comment"))
        self.assertFalse(_match_comment_line(" \t do i=1,100 ! comment"))
        self.assertFalse(_match_comment_line(" \t do i=1,100"))
        self.assertFalse(_match_comment_line("do i=1,100"))
        self.assertFalse(_match_comment_line("integer(8) i"))
        self.assertFalse(_match_comment_line("integer(8) :: i"))
        self.assertFalse(_match_comment_line("integer(8) :: i ! comment"))
        self.assertFalse(_match_comment_line(" \t integer(8) :: i ! comment"))

    def test_variable_colon(self):
        self.assertTrue(_match_variable_colon(" ::"))
        self.assertTrue(_match_variable_colon("blaa ::"))
        self.assertTrue(_match_variable_colon("blaa :: variable"))
        self.assertTrue(_match_variable_colon("blaa :: \t variable"))
        self.assertTrue(_match_variable_colon("blaa \t :: \t variable"))
        self.assertTrue(
            _match_variable_colon("integer(8), intent(in) \t :: \t variable"))
        self.assertTrue(_match_variable_colon("  \t  blaa \t :: \t variable"))

        self.assertFalse(_match_variable_colon("! asldkj"))
        self.assertFalse(_match_variable_colon("  \t ! asldkj"))
        self.assertFalse(_match_variable_colon("  ! integer(8) :: name"))
        self.assertFalse(_match_variable_colon("do i=1,100"))
        self.assertFalse(_match_variable_colon("! do i=1,100"))
