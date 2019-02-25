"""
Command line program & Python functions for comparing multiple dictionaries
===========================================================================

|pypi| |build-status| |coveralls|

`dictsdiff` provides a CLI and Python interface for comparing
arbitrary number of nested dictionaries and show it as a tabular
format via pandas_.DataFrame.


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

   pip install dictsdiff  # or
   pip install https://github.com/tkf/dictsdiff/archive/master.zip


Requirements
^^^^^^^^^^^^

- pandas_
- PyYAML_ (optional)
- toml_ (optional)
- jsonpath-rw_ (optional)

.. _pandas: http://pandas.pydata.org
.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _toml: https://github.com/uiri/toml
.. _jsonpath-rw: https://github.com/kennknowles/python-jsonpath-rw

.. |pypi|
   image:: https://badge.fury.io/py/dictsdiff.svg
   :target: https://badge.fury.io/py/dictsdiff
   :alt: Python Package Index

.. |build-status|
   image:: https://secure.travis-ci.org/tkf/dictsdiff.png?branch=master
   :target: http://travis-ci.org/tkf/dictsdiff
   :alt: Build Status

.. |coveralls|
   image:: https://coveralls.io/repos/github/tkf/dictsdiff/badge.svg?branch=master
   :target: https://coveralls.io/github/tkf/dictsdiff?branch=master
   :alt: Test Coverage
"""

__version__ = '0.1.0'
__author__ = 'Takafumi Arakaki'
__license__ = 'BSD-2-Clause'

from .core import diff_dicts
from .loader import diff_files, diff_ndjson
