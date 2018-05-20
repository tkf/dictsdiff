from itertools import combinations_with_replacement

import pytest

from ..cli import parse_file_paths


@pytest.mark.parametrize('files, desired', [
    ([], []),
    (['a'], [('a', None)]),
    (['a', 'b'], [('a', None), ('b', None)]),
    (['a', '$.b'], [('a', '$.b')]),
    (['a', '$.b', 'c'], [('a', '$.b'), ('c', None)]),
    (['a', '$.b', 'c', '$.d'], [('a', '$.b'), ('c', '$.d')]),
    (['a', 'b', 'c', '$.d'], [('a', None), ('b', None), ('c', '$.d')]),
])
def test_parse_file_paths(files, desired):
    actual = list(parse_file_paths(files))
    assert actual == desired


def gen_file_paths(lengths):
    def gen(length):
        paths = list(map(str, range(length)))
        for isjsp in combinations_with_replacement([False, True], length):
            if any(x and y for x, y in zip(isjsp[:-1], isjsp[1:])):
                # Consecutive JSON_PATH is not allowed; skip it.
                continue

            desired = [(p, '$.' + p if yes else None)
                       for p, yes in zip(paths, isjsp)]

            files = []
            for p, yes in zip(paths, isjsp):
                files.append(p)
                if yes:
                    files.append('$.' + p)

            yield files, desired

    for l in lengths:
        for example in gen(l):
            yield example


def test_parse_file_paths_all(maxlen=5):
    for files, desired in gen_file_paths(range(maxlen + 1)):
        test_parse_file_paths(files, desired)
