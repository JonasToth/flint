#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains useful functions to align some code construct
at a specific character.
"""


def insert_whitespace(line: str, old_anchor: int, new_anchor):
    """
    Insert new whitespace before the old anchor character.

    Example:
    ```
    integer(8) :: i
    !          ^ old anchor
    integer(8)     :: i
    !              ^ new anchor
    ```
    The anchor might be the beginning of `::` that shall be aligned to a
    new position.
    """

    assert old_anchor >= 0
    assert new_anchor >= 0
    necessary_spaces = (new_anchor - old_anchor)
    return line[:old_anchor] + " " * necessary_spaces + line[old_anchor:]


def find_anchor(lines: list, anchor_str: str, skip_regex=None):
    """
    Find the position of the anchor_str (from left) for every line and
    return a list of indices to that anchor.

    :line: list: list of strings that are a line each
    :anchor_str: str: a characteristic string or character, searched from left
    :skip_regex: (compiled) regular expression that initates a line skip
    :returns: list: list of indices the `anchor_str` starts, -1 if not existing
    """
    positions = []
    for line in lines:
        # There might be lines in `lines` that should not count. Filter
        # them with `skip_regex` if wanted.
        if skip_regex and skip_regex(line):
            positions.append(-1)
        else:
            positions.append(line.find(anchor_str))

    return positions
