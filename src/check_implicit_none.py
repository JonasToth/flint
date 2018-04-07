#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for a fortran file if all function constructs
(function, subroutine, program) use `implicit none`.
Fortran modules are not covered yet, because of nesting.
"""

import logging
import re
from file_io import CodeFile
from diagnostics import warning

__regex_start_construct = re.compile(
    r'[^!]*(function|subroutine|program|module)(.*)')
__regex_end_construct = re.compile(
    r'[^!]*end(\s+)(function|subroutine|program|module)(.*)')
__regex_implicit = re.compile(r'[^!]*implicit(\s+)none(.*)')


def _match_implicit(line):
    """
    Match with a regular expression, if the line contains an valid
    'implicit none' statement.

    :line: Arbitrary line of code.
    :returns: True if the line contains a valid (not outcommented)
              'implicit none'.
    """
    if __regex_implicit.match(line):
        return True
    return False


def _match_end_construct(line):
    """
    Match with a regular expression, if the line contains a valid
    ending of a functional construct for 'program', 'function', 'subroutine'
    and 'module'.

    :line: Arbitrary line of code.
    :returns: True if the line contains a valid end construct.
    """
    if __regex_end_construct.match(line):
        return True
    return False


def _match_start_construct(line):
    """
    Match with a regular expression, if the line contains a valid
    beginning of a functional construct for 'program', 'function',
    'subroutine' and 'module'.

    :line: Arbitrary line of code.
    :returns: True if the line contains a valid start construct.
    """
    if __regex_start_construct.match(line):
        return True
    return False


class CheckImplicitNone(object):
    """Check if all code constructs contain `implicit none`."""

    def __init__(self, f_file: CodeFile):
        self._f_file = f_file
        # List of all code locations that do not define `implicit none`.
        self._occurences = []

        self._log = logging.getLogger(__file__ + "::implicit_none")

    def check(self):
        """
        Iterate all function constructs of `f_file` and check if they all
        contain a `implicit none`.
        """
        construct_stack = []

        for (i, line) in enumerate(self._f_file.insensitive_lines(), 1):
            # Check for the implicit none
            if _match_implicit(line):
                self._log.debug("found implicit none with regex")
                self._log.debug(line)

                construct_stack[-1]["implicit_none"] = True
                continue

            # Handle the code construct exit.
            # This must be done first, because the entry would trigger
            # given the string search.
            if _match_end_construct(line):
                self._log.debug("exiting construct")
                self._log.debug(line)

                construct = construct_stack.pop()
                if not construct["implicit_none"]:
                    self._occurences.append(construct["line_start"])
                continue

            # Handle the code construct entry.
            # This is the last state change, because the coarse grain
            # string searching would trigger on 'end function' ...
            if _match_start_construct(line):
                self._log.debug("entering construct")
                self._log.debug(line)

                construct_stack.append({
                    "line_start": i,
                    "implicit_none": False
                })
                continue

    def report(self):
        """
        Emit all warnings for this file.
        """
        for line_nbr in self._occurences:
            warning(self._f_file, line_nbr, "no 'implicit none' found")
