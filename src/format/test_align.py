#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test functionality to align code constructs.
"""

import unittest
from align import insert_whitespace, find_anchor

from common_matcher import match_commented_line


class TestAlign(unittest.TestCase):
    def test_insert_whitespace(self):
        old_line = "integer(8)  :: aksdj"
        new_line = "integer(8)     :: aksdj"
        self.assertEqual(new_line, insert_whitespace(old_line, 12, 15))

        self.assertEqual("     hallo", insert_whitespace("hallo", 0, 5))
        self.assertEqual("hal  lo", insert_whitespace("hallo", 3, 5))

    def test_find_anchor(self):
        self.assertListEqual([], find_anchor([], "::"))
        lines = [
            "some line with :: special _char",
            "anther one :: jo",
            "not contained",
            "aslkdjaslkdj lkajsd lkjasld :: ",
        ]
        self.assertListEqual([15, 11, -1, 28], find_anchor(lines, "::"))

        lines = [
            "some line with :: special _char",
            "anther one :: jo",
            "not contained",
            "aslkdjaslkdj lkajsd lkjasld :: ",
            "!  :: filtered here",
        ]
        self.assertListEqual([15, 11, -1, 28, -1],
                             find_anchor(
                                 lines, "::", skip_regex=match_commented_line))
