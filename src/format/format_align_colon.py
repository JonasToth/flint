#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement a formatter, that aligns the double colon on subsequent lines.

Example:

```fortran
integer(8) :: some_int
real(8) :: some_real
```
becomes
```fortran
integer(8) :: some_int
real(8)    :: some_real
```
"""

import logging
import re

from common_matcher import match_line, match_blank_line, match_commented_line
from common_matcher import match_ignore_single, match_ignore_start,\
                           match_ignore_end
from file_io import CodeFile
from format.abstract_formatter import AbstractFormatter
from format.align import insert_whitespace, find_anchor
from format.utility import overwrite_lines

__regex_variable_colon = re.compile(r'[^!]+::(.*)$')


def _match_variable_colon(line):
    """
    Match if the line is a variable declaration with a double colon.
    This excludes outcommented lines.

    :line: Arbitracy line of code.
    """
    return match_line(__regex_variable_colon, line)


def _align_colons(lines: list):
    """
    Algorithm to align the colons of subsequent lines.

    Requires two passes:
    (1) Find the position of every colon, get the maximum
    (2) Insert whitespace for every smaller colon position
    """

    if len(lines) == 0:
        return []

    colon_position = find_anchor(
        lines,
        "::",
        skip_func=lambda l: match_commented_line(l) or match_ignore_single(l))

    # https://stackoverflow.com/questions/11530799/python-finding-index-of-maximum-in-list
    (max_colon, max_line) = max((v, i) for i, v in enumerate(colon_position))

    formatted_lines = []
    for i, line in enumerate(lines):
        # Only actual variable definitions are reformated.
        if _match_variable_colon(line) and not match_ignore_single(line):
            line = insert_whitespace(line, colon_position[i], max_colon)

        formatted_lines.append(line)

    return formatted_lines


class FormatAlignColon(AbstractFormatter):
    """
    ```fortran
    integer(8) :: some_int
    real(8) :: some_real

    integer(8)   :: another_int
    ! asdojasdlkj
    real(8)  :: and_another_one
    ```
    becomes
    ```fortran
    integer(8) :: some_int
    real(8)    :: some_real

    integer(8)   :: another_int
    ! asdojasdlkj
    real(8)      :: and_another_one
    ```
    Formatting will ignore lines that start with a comment.
    """

    def __init__(self, f_file: CodeFile):
        AbstractFormatter.__init__(self, f_file)

        self._log = logging.getLogger(__file__ + "::align_colon")

    @classmethod
    def help(self):
        return "Align the double colons of subsequent variable definitions."

    def format(self):
        in_decl_list = False
        in_ignore = False
        decl_start = -1
        decl_end = -1

        for (i, line) in enumerate(self._formatted_lines):
            self._log.debug("Line: {}".format(line))

            # Check if the deactivation mechanism matches
            if match_ignore_start(line):
                self._log.debug("start block ignore")
                in_ignore = True

                in_decl_list = False
                decl_start = -1
                decl_end = -1
                continue

            if in_ignore:
                if match_ignore_end(line):
                    self._log.debug("end block ignore")
                    in_ignore = False
                continue

            # Start a declaration section if necessary.
            # If already in a declaration section, continue.
            if _match_variable_colon(line):
                self._log.debug("Found variable declaration with double colon")

                # Either start a declaration section...
                if not in_decl_list:
                    self._log.debug("Starting new decl section at line %d" % i)
                    decl_start = i
                    decl_end = i + 1
                    in_decl_list = True
                # ... or advance its end.
                else:
                    self._log.debug("advancing decl section to line %d" %
                                    (i + 1))
                    decl_end = i + 1
                continue

            # Comments in declaration sections are ignored.
            if match_commented_line(line):
                if in_decl_list:
                    self._log.debug(
                        "skipping comment/blank line in decl section")
                    continue

            # Reaching this line means we are within a declaration section
            # but found neither a declaration line nor a blank/comment line.
            # This means regular code has been reached.
            if in_decl_list:
                self._log.debug("ending declaration section")
                in_decl_list = False
                assert decl_start > 0
                assert decl_end > 0
                new = _align_colons(self._formatted_lines[decl_start:decl_end])

                overwrite_lines(self._formatted_lines, new, decl_start,
                                decl_end)

                decl_start = -1
                decl_end = -1

        return self.formatted_lines()
