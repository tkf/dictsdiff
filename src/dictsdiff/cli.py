"""
Compare multiple similar dictionary data in JSON/YAML/Pickle files.
"""

from __future__ import print_function

import sys


def dictsdiff_cli(files):
    import pandas
    from .loader import diff_files, diff_ndjson

    if files:
        dd = diff_files(files)
    else:
        dd = diff_ndjson(sys.stdin)

    with pandas.option_context('display.max_rows', None,
                               'display.max_columns', None):
        print(dd.diff_df)


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
