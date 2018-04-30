#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement unit tests for the formatter to align trailing comments.
"""

import unittest
from format_trailing_comment import _match_trailing_comment,\
                                    _match_omp_directive


class TestFormatTrailingComment(unittest.TestCase):
    def test_match_trailing_comment(self):
        self.assertTrue(_match_trailing_comment("alskdjlk ! ljasd "))
        self.assertTrue(_match_trailing_comment(" \t alskdjlk! ljasd "))
        self.assertTrue(_match_trailing_comment(" alskdjlk!ljasd "))
        self.assertTrue(_match_trailing_comment(" \"alskdjlk\" !ljasd "))
        self.assertTrue(_match_trailing_comment(" 'alskdjlk' !ljasd "))
        # Its all just for fun...
        # self.assertTrue(_match_trailing_comment(" \"alskdjlk ! \" !ljasd "))
        # self.assertTrue(_match_trailing_comment(" 'alskdjlk ! ' !ljasd "))
        self.assertTrue(_match_trailing_comment(" \"\" !ljasd "))
        self.assertTrue(_match_trailing_comment(" '' !ljasd "))

        self.assertFalse(_match_trailing_comment("! alksjlkd"))
        self.assertFalse(_match_trailing_comment("  ! alksjlkd"))
        self.assertFalse(_match_trailing_comment("  !alksjlkd"))
        self.assertFalse(_match_trailing_comment("  \\!alksjlkd"))
        self.assertFalse(_match_trailing_comment("  \\!"))
        # self.assertFalse(_match_trailing_comment("  \" asdlkj!\""))
        # self.assertFalse(_match_trailing_comment("  ' asdlkj!' asd"))
        self.assertFalse(_match_trailing_comment("  \"\""))
        self.assertFalse(_match_trailing_comment("  ''"))

    def test_match_omp_directive(self):
        self.assertTrue(_match_omp_directive("!$OMP PARALLEL"))
        self.assertTrue(_match_omp_directive("!$OMP"))
        self.assertTrue(_match_omp_directive("!$OMP  "))

        self.assertFalse(_match_omp_directive(" !$OMP"))
        self.assertFalse(_match_omp_directive(" asdlkj !$OMP"))
        self.assertFalse(_match_omp_directive(" $OMP"))
        self.assertFalse(_match_omp_directive("!$ OMP"))
        self.assertFalse(_match_omp_directive("!!$ OMP"))

    def test_block_ignore(self):
        lines = [
            " !&<\n",
            " integer(8), intent(in) :: asldk    ! alksjdasdlj\n",
            " real(8), intent(inout), dimension(10)   :: real_field ! asla \n",
            " !&>\n", 
            "   integer(2) :: flag1  ! and have some weird code\n"
            "   integer(2)   :: flag2  ! and have some weird code\n"
            "   integer(2)     :: flag3  ! and have some weird code\n"
        ]
        expec = [
            " !&<\n",
            " integer(8), intent(in) :: asldk    ! alksjdasdlj\n",
            " real(8), intent(inout), dimension(10)   :: real_field ! asla \n",
            " !&>\n", 
            "   integer(2) :: flag1      ! and have some weird code\n"
            "   integer(2)   :: flag2    ! and have some weird code\n"
            "   integer(2)     :: flag3  ! and have some weird code\n"
        ]
        self.assertListEqual(expec, _align_comments(lines))

    def test_single_ignore(self):
        lines = [
            "   integer(2) :: flag1  ! and have some weird code\n"
            "   integer(2)   :: flag2  !& and have some weird code\n"
            "   integer(2)     :: flag3  ! and have some weird code\n"
        ]
        expec = [
            "   integer(2) :: flag1      ! and have some weird code\n"
            "   integer(2)   :: flag2    !& and have some weird code\n"
            "   integer(2)     :: flag3  ! and have some weird code\n"
        ]
        self.assertListEqual(expec, _align_comments(lines))
