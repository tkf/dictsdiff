"""
Compare multiple similar dictionary data in JSON/YAML/Pickle files.

Usage::

  dictsdiff FILE [JSON_PATH] [FILE [JSON_PATH] ...]
  cat *.ndjson | dictsdiff

When paths to multiple files are given, it loads the dictionaries from
those files and compare (possibly) nested values in them.  The
key-value pairs that are different or missing are shown in a table
format.  A file path ``FILE`` may be followed by a JSONPath_
``JSON_PATH`` which starts with ``$.``.  If ``FILE`` starts with
``$.``, prepend ``./`` to ``FILE`` to disambiguate the argument.
``JSON_PATH`` can be used for non-JSON files.

.. _JSONPath: http://goessner.net/articles/JsonPath/

When no files are given, it is assumed that Newline delimited JSON
(ndjson) is fed to the stdin.

Examples
^^^^^^^^

.. code:: sh

   $ echo '{"a": 1, "b": {"c": 0, "d": 0, "e": 0}}' > 0.json
   $ echo '{"a": 2, "b": {"c": 0, "d": 1, "e": 0}}' > 1.json
   $ echo '{"a": 2, "b": {"c": 0, "d": 1}}' > 2.json
   $ dictsdiff *.json
           a  b.d  b.e
   path
   0.json  1    0  0.0
   1.json  2    1  0.0
   2.json  2    1  NaN
   $ cat *.json | dictsdiff
      a  b.d  b.e
   0  1    0  0.0
   1  2    1  0.0
   2  2    1  NaN

If JSON files are pre-processed by jq_, dictsdiff can handle its
output when ``--compact-output``/``-c`` is passed::

  jq --compact-output '' **/*.json | dictsdiff

.. _jq: https://stedolan.github.io/jq/
"""

from __future__ import print_function

import sys

from .core import DictsDiffError

try:
    from shutil import get_terminal_size
except ImportError:
    def get_terminal_size():
        from subprocess import check_output
        out = check_output(['stty', 'size'], universal_newlines=True)
        rows, columns = map(int, out.strip().split())
        return columns, rows


class CLIError(DictsDiffError, RuntimeError):
    pass


def dictsdiff_cli(files, **kwds):
    import pandas
    from .loader import diff_files, diff_ndjson

    if files:
        dd = diff_files(parse_file_paths(files), **kwds)
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


def parse_file_paths(files):
    """
    Parse FILE argument of the CLI to ``(filepath, jspath)``-tuples.

    >>> list(parse_file_paths(['a', 'b', 'c']))
    [('a', None), ('b', None), ('c', None)]
    >>> list(parse_file_paths(['a', '$.b', 'c']))
    [('a', '$.b'), ('c', None)]
    >>> list(parse_file_paths(['a', '$.b', '$.c']))
    ...                                    # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
       ...
    dictsdiff.cli.CLIError: A JSON_PATH must follow a FILE.
    No FILE is specified before JSON_PATH=$.c.
    If it really is a file path, start it with "./".

    """
    files = iter(files)
    try:
        filepath = next(files)
    except StopIteration:
        return
    while True:
        if filepath.startswith('$.'):
            raise CLIError(
                'A JSON_PATH must follow a FILE.'
                ' No FILE is specified before JSON_PATH={}.'
                ' If it really is a file path, start it with "./".'
                .format(filepath))
        try:
            nextpath = next(files)
        except StopIteration:
            yield (filepath, None)
            return
        if nextpath.startswith('$.'):
            yield (filepath, nextpath)
            try:
                filepath = next(files)
            except StopIteration:
                return
        else:
            yield (filepath, None)
            filepath = nextpath

if sys.version_info[0] == 2:
    parse_file_paths.__doc__ = parse_file_paths.__doc__.replace(
        'dictsdiff.cli.CLIError', 'CLIError')


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
    try:
        dictsdiff_cli(**vars(ns))
    except CLIError as err:
        parser.print_usage()
        parser.exit(2, str(err) + '\n')
    except DictsDiffError as err:
        parser.exit(1, str(err) + '\n')
