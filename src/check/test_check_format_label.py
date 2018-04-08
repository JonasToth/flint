#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for the check to find format labels and its usage.
"""

import logging
from os.path import dirname, join
import re
import unittest
from file_io import CodeFile
from check.check_format_label import _match_format_label, _match_print_label,\
                                     _match_write_label

# logging.basicConfig(level=logging.DEBUG)


class TestCheckFormatLabel(unittest.TestCase):
    def test_match_format_label(self):
        self.assertTrue(_match_format_label("0    format aklsjd"))
        self.assertTrue(_match_format_label("1 \t  format aklsjd"))
        self.assertTrue(_match_format_label("1 format aklsjd"))
        self.assertTrue(_match_format_label("   1 format"))
        self.assertTrue(_match_format_label(" \t 1 format"))
        self.assertTrue(_match_format_label("99999 format aklsjd"))
        self.assertTrue(_match_format_label("99999    format aklsjd"))
        self.assertTrue(_match_format_label("\t 99999    format aklsjd"))
        self.assertTrue(_match_format_label(" 1    format('Threads: ',I4)"))

        self.assertFalse(_match_format_label("! 1 format"))
        self.assertFalse(_match_format_label("format"))
        self.assertFalse(_match_format_label("123456 format"))
        self.assertFalse(_match_format_label("asldkj format"))
        self.assertFalse(_match_format_label("1 ! format"))

    def test_match_print_label(self):
        self.assertTrue(_match_print_label("print 12"))
        self.assertTrue(_match_print_label(" print 12"))
        self.assertTrue(_match_print_label(" \t print 12"))
        self.assertTrue(_match_print_label("  print 12, \"Jo\""))
        self.assertTrue(_match_print_label("  print 12 , \"Jo\""))
        self.assertTrue(_match_print_label("  print 12 , \"Jo\" ! comment"))

        self.assertFalse(_match_print_label(" print 123456"))
        self.assertFalse(_match_print_label("print 123456"))
        self.assertFalse(_match_print_label("print 123456, \"Jo\" ! comment"))
        self.assertFalse(_match_print_label("print 123456 , \"Jo\" ! comment"))
        self.assertFalse(_match_print_label("  print 123456 , \"Jo\" ! "))

        self.assertFalse(_match_print_label("! print 12"))
        self.assertFalse(_match_print_label("  ! print 123"))
        self.assertFalse(_match_print_label("  ! print 123"))
        self.assertFalse(_match_print_label("  ! print 123 ,  \"asllkdj\" "))

    def test_match_write_label(self):
        self.assertTrue(_match_write_label("write(*,12)"))
        self.assertTrue(_match_write_label(" \t write(*,12)"))
        self.assertTrue(_match_write_label(" \t write(*,FMT=12)"))
        self.assertTrue(_match_write_label(" \t write(*,  FMT  =\t12)"))
        self.assertTrue(_match_write_label(" \t write  (* ,   12   )"))
        self.assertTrue(_match_write_label(" \t write  ( aslkdj ,   12   )"))
        self.assertTrue(_match_write_label(" write  ( * , 12 )something"))
        self.assertTrue(_match_write_label(" write  ( aslkdj ,   12   )"))
        self.assertTrue(_match_write_label(" write  ( * , 12 )something, else"))
        self.assertTrue(_match_write_label(" write  ( aslkdj ,   12   ) alsd ! las"))

        self.assertFalse(_match_write_label("write(*,121235)"))
        self.assertFalse(_match_write_label(" \t write(*,*)"))
        self.assertFalse(_match_write_label(" \t write(*)"))
        self.assertFalse(_match_write_label(" \t write(*,  FMT  =\t121239)"))
        self.assertFalse(_match_write_label("! write(*,12)"))
        self.assertFalse(_match_write_label(" \t  ! write(*,12)"))
        self.assertFalse(_match_write_label("! \t write(*,FMT=12)"))
        self.assertFalse(_match_write_label(" \t write  (* , 123012   )"))
        self.assertFalse(_match_write_label("something unrelated, with write"))

