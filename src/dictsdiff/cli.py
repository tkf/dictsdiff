"""
Compare multiple similar dictionary data in JSON/YAML/Pickle files.

Usage::

  dictsdiff FILE [FILE ...]
  cat *.ndjson | dictsdiff

When paths to multiple files are given, it loads the dictionaries from
those files and compare (possibly) nested values in them.  The
key-value pairs that are different or missing are shown in a table
format.

When no files are given, it is assumed that Newline delimited JSON
(ndjson) is fed to the stdin.
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


def dictsdiff_cli(files, **kwds):
    import pandas
    from .loader import diff_files, diff_ndjson

    if files:
        dd = diff_files(files, **kwds)
    else:
        dd = diff_ndjson(sys.stdin, **kwds)

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
    parser.add_argument(
        '--atol', default=0, type=float,
        help='''
        When `atol` or `rtol` is non-zero, then the comparison of the
        floating point values are done using the following equation:
        ``|a - b| <= atol + rtol * |b|`` where `a` is the value in the
        first dictionary (file).  Comparison of the non-floating point
        value is not affected.
        ''')
    parser.add_argument(
        '--rtol', default=0, type=float,
        help='See --atol.')
    return parser


def main(args=None):
    parser = make_parser()
    ns = parser.parse_args(args)
    dictsdiff_cli(**vars(ns))
