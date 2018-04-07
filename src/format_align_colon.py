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
from file_io import CodeFile

__regex_blank_line = re.compile(r'^(\s*)$')
__regex_comment_line = re.compile(r'^(\s*)!(.*)$')
__regex_variable_colon = re.compile(r'[^!]+::(.*)$')


def _match_blank_line(line):
    """
    Match with a regular expression, if `line` is blank.
    This means only whitespace is allowed on the line.

    :line: Arbitrary line of code.
    :returns: True if the line is blank.
    """
    if __regex_blank_line.match(line):
        return True
    return False


def _match_comment_line(line):
    """
    Match with a regular expression, if `line` contains only a comment.
    Trailing comments are not matched!

    :line: Arbitrary line of code.
    :returns: True if the contains only a comment
    """
    if __regex_comment_line.match(line):
        return True
    return False


def _match_variable_colon(line):
    """
    Match if the line is a variable declaration with a double colon.
    This excludes outcommented lines.

    :line: Arbitracy line of code.
    """
    if __regex_variable_colon.match(line):
        return True
    return False


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

    @classmethod
    def help(self):
        return "Align the double colons of subsequent variable definitions."

    def format(self):
        pass
