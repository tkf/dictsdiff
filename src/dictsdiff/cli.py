"""
Compare multiple similar dictionary data in JSON/YAML/Pickle files.
"""

from __future__ import print_function

import sys

try:
    from shutil import get_terminal_size
except ImportError:
    def get_terminal_size():
        from subprocess import check_output
        out = check_output(['stty', 'size'], universal_newlines=True)
        rows, columns = map(int, out.strip().split())
        return columns, rows


def dictsdiff_cli(files):
    import pandas
    from .loader import diff_files, diff_ndjson

    if files:
        dd = diff_files(files)
    else:
        dd = diff_ndjson(sys.stdin)

    # Manually detect terminal size, since passing "'display.width',
    # None" does not detect terminal size (as advertised in
    # https://pandas.pydata.org/pandas-docs/stable/options.html):
    width, _ = get_terminal_size()

    with pandas.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', width):
        print(dd.pretty_diff())


def make_parser(doc=__doc__):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=type('FormatterClass',
                             (argparse.RawDescriptionHelpFormatter,
                              argparse.ArgumentDefaultsHelpFormatter),
                             {}),
        description=doc)
    parser.add_argument(
        'files', metavar='FILE', nargs='*',
    )
    return parser


def main(args=None):
    parser = make_parser()
    ns = parser.parse_args(args)
    dictsdiff_cli(**vars(ns))
