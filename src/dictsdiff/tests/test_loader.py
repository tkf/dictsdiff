import pickle

from ..loader import load_any


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
