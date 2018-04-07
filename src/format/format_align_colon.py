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

from abstract_formatter import AbstractFormatter
from common_matcher import match_line, match_blank_line, match_commented_line
from file_io import CodeFile

__regex_variable_colon = re.compile(r'[^!]+::(.*)$')


def _match_variable_colon(line):
    """
    Match if the line is a variable declaration with a double colon.
    This excludes outcommented lines.

    :line: Arbitracy line of code.
    """
    return match_line(__regex_variable_colon, line)


def _align_colons(lines):
    """
    Algorithm to align the colons of subsequent lines.

    Requires two passes:
    (1) Find the position of every colon, get the maximum
    (2) Insert whitespace for every smaller colon position
    """

    if len(lines) == 0:
        return []

    formatted_lines = []
    colon_position = []

    for line in lines:
        # Comments could contain '::' and might confuse the algorithm.
        if _match_variable_colon(line):
            colon_position.append(line.find("::"))
        else:
            colon_position.append(0)

    # https://stackoverflow.com/questions/11530799/python-finding-index-of-maximum-in-list
    (max_colon, max_line) = max((v, i) for i, v in enumerate(colon_position))

    for i, line in enumerate(lines):
        # Only actual variable definitions are reformated.
        if _match_variable_colon(line):
            col_position = colon_position[i]

            necessary_spaces = (max_colon - col_position)

            # The line must be put together again with potentially
            # added whitespace.
            line = line[:col_position] +\
                   " " * necessary_spaces +\
                   line[col_position:]

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
    integer(8)   :: some_int
    real(8)      :: some_real

    integer(8)   :: another_int
    ! asdojasdlkj
    real(8)      :: and_another_one
    ```
    Formatting will ignore blank lines and lines that start with a comment.
    """

    def __init__(self, f_file: CodeFile):
        AbstractFormatter.__init__(self, f_file)

        self._log = logging.getLogger(__file__ + "::align_colon")

    @classmethod
    def help(self):
        return "Align the double colons of subsequent variable definitions."

    def format(self):
        in_decl_list = False
        decl_start = -1
        decl_end = -1

        for (i, line) in enumerate(self._formatted_lines):
            self._log.debug("Line: {}".format(line))
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

            # Blank lines and comments in declaration sections are ignored.
            if match_blank_line(line) or\
               match_commented_line(line):
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
                assert decl_start >= 0
                assert decl_end >= 0
                new = _align_colons(self._formatted_lines[decl_start:decl_end])

                # Overwrite for formatting.
                for new_line_idx, old_line_idx in enumerate(
                        range(decl_start, decl_end)):
                    self._log.debug("Overwriting:")
                    self._log.debug("Old: {}".format(
                        self._formatted_lines[old_line_idx]))
                    self._log.debug("New: {}".format(new[new_line_idx]))
                    self._formatted_lines[old_line_idx] = new[new_line_idx]

                decl_start = -1
                decl_end = -1

        return self.formatted_lines()
