#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for a fortran file if all function constructs
(function, subroutine, program) use `implicit none`.
Fortran modules are not covered yet, because of nesting.
"""

import logging
import re

from check.abstract_check import AbstractCheck
from common_matcher import match_line, match_begin_block, match_end_block
from file_io import CodeFile
from diagnostics import warning

__regex_implicit = re.compile(r'[^!]*implicit(\s+)none(.*)')


def _match_implicit(line):
    """
    Match with a regular expression, if the line contains an valid
    'implicit none' statement.

    :line: Arbitrary line of code.
    :returns: True if the line contains a valid (not outcommented)
              'implicit none'.
    """
    return match_line(__regex_implicit, line)


class CheckImplicitNone(AbstractCheck):
    """Check if all code constructs contain `implicit none`."""

    def __init__(self, f_file: CodeFile):
        super(CheckImplicitNone, self).__init__(f_file)

        # List of all code locations that do not define `implicit none`.
        self._occurences = []
        self._log = logging.getLogger(__file__ + "::implicit_none")

    @classmethod
    def help(self):
        return "Warn if 'implicit none' is not used"

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
                assert len(construct_stack) > 0

                construct_stack[-1]["implicit_none"] = True
                continue

            # Handle the code construct exit.
            # This must be done first, because the entry would trigger
            # given the string search.
            if match_end_block(line):
                self._log.debug("exiting construct")
                self._log.debug(line)

                construct = construct_stack.pop()
                if not construct["implicit_none"]:
                    self._occurences.append(construct["line_start"])
                continue

            # Handle the code construct entry.
            # This is the last state change, because the coarse grain
            # string searching would trigger on 'end function' ...
            if match_begin_block(line):
                self._log.debug("entering construct")
                self._log.debug(line)

                construct_stack.append({
                    "line_start": i,
                    "implicit_none": False
                })
                continue

        assert len(construct_stack) == 0

    def report(self):
        """
        Emit all warnings for this file.
        """
        for line_nbr in self._occurences:
            warning(self._f_file, line_nbr, "no 'implicit none' found")
