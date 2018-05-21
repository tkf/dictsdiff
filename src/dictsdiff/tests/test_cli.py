from itertools import combinations_with_replacement
import os

import pytest

from ..cli import parse_file_paths, main


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


@pytest.mark.parametrize('options', [
    [],
    ['-T'],
    ['--transform', 'cat {}'],
])
def test_main_smoke(tmpdir, options):
    paramfile1 = tmpdir.join('param1.json')
    paramfile2 = tmpdir.join('param2.json')
    paramfile1.write('{"x": 1}')
    paramfile2.write('{"x": 2}')
    main(options + [str(paramfile1), str(paramfile2)])


def test_main_smoke_ndjson(tmpdir):
    paramfile = tmpdir.join('param.ndjson')
    paramfile.write('''
    {"x": 1}
    {"x": 2}
    '''.strip())
    main(['--ndjson', str(paramfile)])


def test_ndjson_and_files(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(['--ndjson=-', os.devnull])
    captured = capsys.readouterr()
    assert excinfo.value.code == 2
    assert 'FILES and --ndjson are mutually exclusive.' in captured.err


def test_load_error(capsys, tmpdir):
    paramfile = tmpdir.join('file.!unknown_extension!')
    paramfile.write('!')  # invalid as JSON
    with pytest.raises(SystemExit) as excinfo:
        main([str(paramfile)])
    captured = capsys.readouterr()
    assert excinfo.value.code == 1
    assert 'is not supported' in captured.err
