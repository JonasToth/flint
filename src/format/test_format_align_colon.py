#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test if all functions to align the double colon on subsequent lines do
work as expected.
"""

import logging
from os.path import dirname, join
import unittest

from file_io import CodeFile, FortranCode
from format.format_align_colon import _match_variable_colon, _align_colons,\
                                      FormatAlignColon

# logging.basicConfig(level=logging.DEBUG)


class TestFormatAlignColor(unittest.TestCase):
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
            " integer(8), intent(in) :: asldk\n",
            " ! We can define reals, too\n",
            " real(8), intent(inout), dimension(10)   :: real_field\n",
            "   integer(2) :: flag  ! and have some weird code\n"
        ]
        expec = [
            " integer(8), intent(in)                  :: asldk\n",
            " ! We can define reals, too\n",
            " real(8), intent(inout), dimension(10)   :: real_field\n",
            "   integer(2)                            :: flag  ! and have some weird code\n"
        ]
        self.assertListEqual(expec, _align_colons(lines))

    def test_block_ignore(self):
        lines = [
            " !&<\n",
            " integer(8), intent(in) :: asldk\n",
            " real(8), intent(inout), dimension(10)   :: real_field\n",
            " !&>\n",
            "   integer(2) :: flag1  ! and have some weird code\n",
            "   integer(2)   :: flag2  ! and have some weird code\n",
            "   integer(2)     :: flag3  ! and have some weird code\n",
        ]
        f_file = FortranCode(lines)
        f = FormatAlignColon(f_file)
        f.format()
        result = f.formatted_lines()

        expec = [
            " !&<\n",
            " integer(8), intent(in) :: asldk\n",
            " real(8), intent(inout), dimension(10)   :: real_field\n",
            " !&>\n",
            "   integer(2)     :: flag1  ! and have some weird code\n",
            "   integer(2)     :: flag2  ! and have some weird code\n",
            "   integer(2)     :: flag3  ! and have some weird code\n",
        ]
        self.assertListEqual(expec, result)

    def test_single_ignore(self):
        lines = [
            "   integer(2) :: flag1  ! and have some weird code\n",
            "   integer(2)   :: flag2  !& and have some weird code\n",
            "   integer(2)     :: flag3  ! and have some weird code\n",
        ]
        expec = [
            "   integer(2)     :: flag1  ! and have some weird code\n",
            "   integer(2)   :: flag2  !& and have some weird code\n",
            "   integer(2)     :: flag3  ! and have some weird code\n",
        ]
        self.assertListEqual(expec, _align_colons(lines))

    def test_real_formatting(self):
        f_file = CodeFile(
            join(dirname(__file__), "../../test/format/format_real.f90"))
        f = FormatAlignColon(f_file)
        expected = [
            "  subroutine locate(l,n,array,var,pos)\n",
            "    !> Search the index of given value in sorted 1D array of unique values.\n",
            "    !>\n",
            "    !> It uses a binary search algorithm.\n",
            "    implicit none\n",
            "    integer(int_p), intent(in)             :: l !> Initial guess of lower limit.\n",
            "    integer(int_p), intent(in)             :: n !> Size of array.\n",
            "    real(real_p), dimension(n), intent(in) :: array !> Sorted array to search.\n",
            "    real(real_p), intent(in)               :: var !> Value to find.\n",
            "    integer(int_p), intent(out)            :: pos !> Resulting index.\n",
            "\n",
            "    ! interrupting comment\n",
            "\n",
            "    integer(int_p) :: jl !> Lower limit.\n",
            "    integer(int_p) :: jm !> Midpoint\n",
            "    integer(int_p) :: ju !> Upper limit\n",
            "    ! Initialize lower limit (L=0 FOR A NORMAL VECTOR!).\n",
            "    jl=l\n",
            "    ! Initialize upper limit.\n",
            "    ju=jl+n+1\n",
            "    ! If we are not yet done compute a midpoint.\n",
            "    pos=max(l+1,pos)\n",
            "    return\n",
            "  end subroutine locate\n",
            "\n",
            "\n",
            "  pure function equal(arg1,arg2) result(res)\n",
            "      !> Returns whether the arguments are equal to machine precision\n",
            "      real(real_p), intent(in) :: arg1, arg2\n",
            "      logical                  :: res\n",
            "      res = (abs(arg1-arg2) < REALTOL)\n",
            "  end function equal\n",
            "\n",
            "  subroutine print_assertion_error(filename, line, error_msg)\n",
            "    implicit none\n",
            "\n",
            "    character(len=*), intent(in) :: filename\n",
            "    integer(int_p), intent(in)   :: line\n",
            "    character(len=*), intent(in) :: error_msg\n",
            "    character(len=10)            :: line_string\n",
            "\n",
            "    write (line_string, '(I2)') line\n",
            "    write (*,*) trim(filename) // \": \" // trim(line_string) // \": \" // trim(error_msg)\n",
            "  end subroutine print_assertion_error\n"
        ]
        f.format()
        new_file = f.formatted_lines()

        self.assertListEqual(expected, new_file)
