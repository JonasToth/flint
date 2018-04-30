#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file consists of common line matchers that are useful in all modules.
"""

import re


def match_line(regex, line):
    """
    Match a line with a specific regular expression and return True
    if the regex did match.

    :regex: a compiled regular expression
    :line: arbitrary line of code
    :returns: boolean if the regex did match the line
    """
    if regex.match(line):
        return True

    return False


__regex_begin_block = re.compile(
    r'(^\s*|^[^!]*\s+)(function|subroutine|program|module)\s+(.*)$')
__regex_end_block = re.compile(
    r'^[^!]*end(\s+)(function|subroutine|program|module)(.*)$')

def match_begin_block(line):
    return match_line(__regex_begin_block, line)

def match_end_block(line):
    return match_line(__regex_end_block, line)


__regex_blank_line = re.compile(r'^(\s*)$')
__regex_comment_line = re.compile(r'^(\s*)!(.*)$')

def match_blank_line(line):
    return match_line(__regex_blank_line, line)

def match_commented_line(line):
    return match_line(__regex_comment_line, line)


__regex_begin_ignore = re.compile(r'^\s*(!&<).*$')
__regex_end_ignore = re.compile(r'^\s*(!&>).*$')
__regex_single_ignore = re.compile(r'^[^!]*!&[^<>]*$')

def match_ignore_single(line):
    return match_line(__regex_single_ignore, line)

def match_ignore_start(line):
    return match_line(__regex_begin_ignore, line)

def match_ignore_end(line):
    return match_line(__regex_end_ignore, line)
