#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test if all functions to align the double colon on subsequent lines do
work as expected.
"""

import logging
from os.path import dirname, join
import unittest

from file_io import CodeFile
from format_align_colon import _match_blank_line, _match_comment_line,\
                               _match_variable_colon, _align_colons,\
                               FormatAlignColon

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

    def test_two_line_alignment(self):
        two_lines = [
            " asdlkfjldsflj :: aslkdjasldk", " kajsdj :: alsjdlkajdoi"
        ]
        self.assertListEqual([
            " asdlkfjldsflj :: aslkdjasldk", " kajsdj        :: alsjdlkajdoi"
        ], _align_colons(two_lines))
        two_lines = [
            " asdlkfjldsflj    :: aslkdjasldk", " kajsdj :: alsjdlkajdoi"
        ]
        self.assertListEqual([
            " asdlkfjldsflj    :: aslkdjasldk",
            " kajsdj           :: alsjdlkajdoi"
        ], _align_colons(two_lines))
        two_lines = [
            " asdlkfjldsflj    ::   aslkdjasldk", " kajsdj :: alsjdlkajdoi"
        ]
        self.assertListEqual([
            " asdlkfjldsflj    ::   aslkdjasldk",
            " kajsdj           :: alsjdlkajdoi"
        ], _align_colons(two_lines))

    def test_single_line_alignment(self):
        line = [" alksjd :: asdlkj"]
        self.assertListEqual(line, _align_colons(line))
        line = [" alksjdasdlkj"]
        self.assertListEqual(line, _align_colons(line))

    def test_complex_alignment(self):
        lines = [
            " integer(8), intent(in) :: asldk", " ! We can define reals, too",
            " real(8), intent(inout), dimension(10)   :: real_field", "",
            "     ", "  ! or even something like this",
            "   integer(2) :: flag  ! and have some weird code"
        ]
        expec = [
            " integer(8), intent(in)                  :: asldk",
            " ! We can define reals, too",
            " real(8), intent(inout), dimension(10)   :: real_field", "",
            "     ", "  ! or even something like this",
            "   integer(2)                            :: flag  ! and have some weird code"
        ]
        self.assertListEqual(expec, _align_colons(lines))

    def test_real_formatting(self):
        f_file = CodeFile(
            join(dirname(__file__), "../test/format/format_real.f90"))
        f = FormatAlignColon(f_file)
        expected = [
            "  subroutine locate(l,n,array,var,pos)",
            "    !> Search the index of given value in sorted 1D array of unique values.",
            "    !>",
            "    !> It uses a binary search algorithm.",
            "    implicit none",
            "    integer(int_p), intent(in)             :: l !> Initial guess of lower limit.",
            "    integer(int_p), intent(in)             :: n !> Size of array.",
            "    real(real_p), dimension(n), intent(in) :: array !> Sorted array to search.",
            "    real(real_p), intent(in)               :: var !> Value to find.",
            "    integer(int_p), intent(out)            :: pos !> Resulting index.",
            "",
            "    ! interrupting comment",
            "",
            "    integer(int_p)                         :: jl !> Lower limit.",
            "    integer(int_p)                         :: jm !> Midpoint",
            "    integer(int_p)                         :: ju !> Upper limit",
            "    ! Initialize lower limit (L=0 FOR A NORMAL VECTOR!).",
            "    jl=l",
            "    ! Initialize upper limit.",
            "    ju=jl+n+1",
            "    ! If we are not yet done compute a midpoint.",
            "    pos=max(l+1,pos)",
            "    return",
            "  end subroutine locate",
            "",
            "",
            "  pure function equal(arg1,arg2) result(res)",
            "      !> Returns whether the arguments are equal to machine precision",
            "      real(real_p), intent(in) :: arg1, arg2",
            "      logical                  :: res",
            "      res = (abs(arg1-arg2) < REALTOL)",
            "  end function equal",
            "",
            "  subroutine print_assertion_error(filename, line, error_msg)",
            "    implicit none",
            "",
            "    character(len=*), intent(in) :: filename",
            "    integer(int_p), intent(in)   :: line",
            "    character(len=*), intent(in) :: error_msg",
            "    character(len=10)            :: line_string",
            "",
            "    write (line_string, '(I2)') line",
            "    write (*,*) trim(filename) // \": \" // trim(line_string) // \": \" // trim(error_msg)",
            "  end subroutine print_assertion_error"
        ]
        f.format()
        new_file = f.formatted_lines()

        self.assertListEqual(expected, new_file)
