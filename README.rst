Command line program & Python functions for comparing multiple dictionaries
===========================================================================

`dictsdiff` provides a CLI and Python interface for comparing
arbitrary number of nested dictionaries and show it as a tabular
format via pandas_.DataFrame.


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


Python interface
----------------

`dictsdiff.diff_dicts`
^^^^^^^^^^^^^^^^^^^^^^

>>> from dictsdiff import diff_dicts
>>> dd = diff_dicts([
...     {'a': 1, 'b': {'c': 0, 'd': 0}},
...     {'a': 2, 'b': {'c': 0, 'd': 1}},
...     {'a': 1, 'b': {'c': 0, 'd': 1}},
... ])
>>> dd.keys
[('a',), ('b', 'd')]
>>> dd.pretty_diff()
   a  b.d
0  1    0
1  2    1
2  1    1


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


Installation
------------
::

   pip install https://github.com/tkf/dictsdiff/archive/master.zip


Requirements
^^^^^^^^^^^^

- pandas_
- PyYAML_ (optional)

.. _pandas: http://pandas.pydata.org
.. _PyYAML: http://pyyaml.org/wiki/PyYAML
