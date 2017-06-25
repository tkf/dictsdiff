Command line program & Python functions for comparing multiple dictionaries
===========================================================================

CLI
---

Usage::

  dictsdiff FILE [FILE ...]
  cat *.ndjson | dictsdiff

When paths to multiple files are given, it loads the dictionaries from
those files and compare (possibly) nested values in them.  The
key-value pairs that are different or missing are shown in a table
format.

When no files are given, it is assumed that Newline delimited JSON
(ndjson) is fed to the stdin.


Python interface
----------------

`dictsdiff.diff_dicts`
^^^^^^^^^^^^^^^^^^^^^^

>>> from dictsdiff import diff_dicts
>>> dd = diff_dicts([
...     {'a': 1, 'b': {'c': 0, 'd': 0}},
...     {'a': 2, 'b': {'c': 0, 'd': 1}},
... ])
>>> dd.keys
[('a',), ('b', 'd')]
>>> dd.pretty_diff()
   a  b.d
0  1    0
1  2    1


`dictsdiff.diff_files`
^^^^^^^^^^^^^^^^^^^^^^

.. Run the code below in a clean temporary directory:
   >>> getfixture('cleancwd')

>>> from dictsdiff import diff_files
>>> _ = open('0.json', 'w').write('{"a": 1, "b": 2}')
>>> _ = open('1.json', 'w').write('{"a": 1, "b": 3}')
>>> dd = diff_files(['0.json', '1.json'])
>>> dd.keys
[('b',)]
>>> dd.pretty_diff()
        b
path     
0.json  2
1.json  3


`dictsdiff.diff_ndjson`
^^^^^^^^^^^^^^^^^^^^^^^

>>> import io
>>> from dictsdiff import diff_ndjson
>>> ndjson = u'''
... {"a": 1, "b": {"c": 0, "d": 0}}
... {"a": 2, "b": {"c": 0, "d": 1}}
... '''.strip()
>>> dd = diff_ndjson(io.StringIO(ndjson))
>>> dd.keys
[('a',), ('b', 'd')]
>>> dd.pretty_diff()
   a  b.d
0  1    0
1  2    1
