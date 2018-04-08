#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for format labels and warn for all `write` statements that use
such a format label.
"""

import logging
import re

from check.abstract_check import AbstractCheck
from common_matcher import match_line, match_begin_block, match_end_block
from file_io import CodeFile
from diagnostics import warning, note

REGEX_FORMAT_LABEL = re.compile(r'^(\s*)(\w{1,5})(\s+)format(.*)$')
REGEX_PRINT_LABEL = re.compile(r'^(\s*)print(\s+)(\w{1,5})(\s*,.*)?$')
REGEX_WRITE_LABEL = re.compile(
    r'^(\s*)write(\s*)\([^,]+,(\s*FMT\s*\=)?\s*(\w{1,5})(\s*)\)(.*)$')


def _match_format_label(line):
    """
    Match if a line specifies a format label.
    """
    return match_line(REGEX_FORMAT_LABEL, line)


def _match_print_label(line):
    """
    Match if a `PRINT` statement uses a format label.
    """
    return match_line(REGEX_PRINT_LABEL, line)


def _match_write_label(line):
    """
    Match if a `WRITE` statement uses a format label.
    """
    return match_line(REGEX_WRITE_LABEL, line)


class CheckFormatLabel(AbstractCheck):
    """Warn for all `FORMAT` labels and its uses in `WRITE` statements."""

    def __init__(self, f_file: CodeFile):
        super(CheckFormatLabel, self).__init__(f_file)

        # Map all defined format labels to a list of its usages.
        # This mapping is done for each code block because labels might
        # be reused in other functions?!
        self._label_map = []
        self._log = logging.getLogger(__file__ + "::format_label")

    @classmethod
    def help(self):
        return "Warn for all `FORMAT` labels and its usage."

    def check(self):
        """
        Iterate all functional blocks and analyze each of them for format
        labels and/or write statements that use a format label.
        """
        construct_stack = []

        for (i, line) in enumerate(self._f_file.insensitive_lines(), 1):
            # Detect definiton of format label
            if _match_format_label(line):
                match = REGEX_FORMAT_LABEL.match(line)
                label_number = int(match.group(2))

                # self._log.debug("adding definiton at %d" % i)
                d = _add_label_definition(construct_stack[-1]["block_info"],
                                          label_number, i)
                construct_stack[-1]["block_info"] = d
                continue

            # Detect uses of labels in `PRINT` statements.
            if _match_print_label(line):
                match = REGEX_PRINT_LABEL.match(line)
                label_number = int(match.group(3))

                # self._log.debug("adding user at %d" % i)
                d = _add_label_user(construct_stack[-1]["block_info"],
                                    label_number, i)
                construct_stack[-1]["block_info"] = d
                continue

            # Detect uses of labels in `WRITE` statements.
            if _match_write_label(line):
                match = REGEX_WRITE_LABEL.match(line)
                label_number = int(match.group(4))

                # self._log.debug("adding user at %d" % i)
                d = _add_label_user(construct_stack[-1]["block_info"],
                                    label_number, i)
                construct_stack[-1]["block_info"] = d
                continue

            # End of Construct means the same labels can be used in another
            # block. To prevent confusion, pop the stack and work the
            # block_info from the construct below.
            if match_end_block(line):
                # Append this block and all its labels to all occurences
                # if necessary.
                construct = construct_stack.pop()
                self._log.debug("removing block at %d" % i)
                if construct["block_info"]:
                    self._log.debug("Found format labels in this section")
                    self._label_map.append(construct["block_info"])
                continue

            if match_begin_block(line):
                self._log.debug("adding block at %s" % i)
                construct_stack.append({"line_start": i, "block_info": None})
                continue

        assert len(construct_stack) == 0

    def report(self):
        for block in self._label_map:
            for format_label, info in block.items():
                warning(self._f_file, info["definition"],
                        "defined format label '{}' here".format(format_label))

                for used_at in info["users"]:
                    note(self._f_file, used_at, "used this label here")


def _add_label_user(block_info, label_number, used_at):
    if block_info is None:
        block_info = _create_block_info(label_number)

    if label_number in block_info:
        block_info[label_number]["users"].append(used_at)
    else:
        block_info[label_number] = {
            "definition": -1,
            "users": [
                used_at,
            ]
        }

    return block_info


def _add_label_definition(block_info, label_number: int, defined_at: int):
    if block_info is None:
        block_info = _create_block_info(label_number)

    if label_number in block_info:
        assert block_info[label_number]["definition"] == -1
        block_info[label_number]["definition"] = defined_at
    else:
        block_info[label_number] = {"definition": defined_at, "users": []}

    return block_info


def _create_block_info(label_number: int):
    """Return one information dict for a format label."""
    return {label_number: {"definition": -1, "users": []}}
