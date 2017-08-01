import pickle

import pytest

from ..loader import load_any, to_info_dict


def test_load_yaml(tmpdir):
    paramfile = tmpdir.join('param.yaml')
    paramfile.write('x: 1')
    loaded = load_any(str(paramfile))
    assert loaded == {'x': 1}


def test_load_json(tmpdir):
    paramfile = tmpdir.join('param.json')
    paramfile.write('{"x": 1}')
    loaded = load_any(str(paramfile))
    assert loaded == {'x': 1}


def test_load_pickle(tmpdir):
    paramfile = tmpdir.join('param.pickle')
    dumped = {'x': 1}
    with open(str(paramfile), 'wb') as file:
        pickle.dump(dumped, file)
    loaded = load_any(str(paramfile))
    assert loaded == dumped


def test_load_toml(tmpdir):
    paramfile = tmpdir.join('param.toml')
    paramfile.write('x = 1')
    loaded = load_any(str(paramfile))
    assert loaded == {'x': 1}


@pytest.mark.parametrize('path, info_dict', [
    ('strpath', dict(path='strpath', filepath='strpath')),
    (('strpath', None), dict(path='strpath', filepath='strpath')),
    (('strpath', 'jspath'), dict(path='strpath jspath', filepath='strpath',
                                 jsonpath='jspath')),
])
def test_to_info_dict(path, info_dict):
    actual = to_info_dict(path)
    assert isinstance(actual['path'], str)
    assert actual == info_dict
