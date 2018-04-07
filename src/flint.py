#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executable that uses the implemented checks.
"""

import argparse
import sys

from check_implicit_none import CheckImplicitNone
from file_io import CodeFile


def handle_analysis(args):
    """
    Implement all static analysis related functions

    :args: Command line arguments passed to the command.
    """
    all_checks = {
        "implicit-none": CheckImplicitNone,
    }

    # If listing is wanted, only that will be done.
    if args.list:
        for name, class_ref in all_checks.items():
            print("{}: {}".format(name, class_ref.help()))
            return

    # Reaching this point means, static analysis shall be done.
    # There is a default list of checks.
    assert args.checks, "Logic error!"

    # Separate the list of checks and ensure they do exist.
    enabled_checks = args.checks.split(",")
    for check in enabled_checks:
        if check not in all_checks:
            print(
                "Configured check '{}' does not exist!".format(check),
                file=sys.stderr)
            sys.exit(1)

    if not args.files:
        print("Provide at least one file for analysis!", file=sys.stderr)
        sys.exit(1)


    for file in args.files:
        f_file = CodeFile(file)
        for check in enabled_checks:
            check_instance = all_checks[check](f_file)
            check_instance.check()
            check_instance.report()


def handle_formatting(args):
    """
    Implement all formatting related functions

    :args: Command line arguments passed to the command.
    """
    print(args)


def main():
    """
    Run the configured static analysis over a specified list of files.
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parse_check = subparser.add_parser("check", help="do static analysis")
    parse_check.add_argument(
        "-c",
        "--checks",
        type=str,
        default="implicit-none",
        help="Comma separated list of checks to enable.")
    parse_check.add_argument(
        "-l", "--list", action="store_true", help="List all available checks.")
    parse_check.add_argument(
        "files", nargs="*", help="List of fortran files to analyse")
    parse_check.set_defaults(func=handle_analysis)

    parse_format = subparser.add_parser("format", help="Format Code")
    parse_format.add_argument(
        "-f",
        "--formatters",
        type=str,
        nargs=1,
        help="Comma separated list of formatters to apply in the given order.")
    parse_format.set_defaults(func=handle_formatting)

    args = parser.parse_args()

    if vars(args):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
