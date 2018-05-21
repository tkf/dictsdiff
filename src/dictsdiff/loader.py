import os
import subprocess
import sys

from .core import DictsDiffError, DictsDiff, diff_dicts


class LoaderError(DictsDiffError):
    pass


def param_module(path):
    if path.lower().endswith(('.yaml', '.yml')):
        import yaml
        return yaml, ''
    elif path.lower().endswith('.json'):
        import json
        return json, ''
    elif path.lower().endswith(('.pickle', '.pkl')):
        try:
            import cPickle as pickle
        except:
            import pickle
        return pickle, 'b'
    elif path.lower().endswith('.toml'):
        import toml
        return toml, ''
    else:
        raise LoaderError(
            'data format of {!r} is not supported'.format(path))


def load_any_file(path):
    """
    Load data from given path; data format is determined by file extension
    """
    import json
    try:
        from json import JSONDecodeError
    except ImportError:
        JSONDecodeError = ValueError  # Python 2

    try:
        module, mode = param_module(path)
    except LoaderError as err:
        # Try to load as JSON anyway:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (OSError, IOError, JSONDecodeError):
            pass
        if sys.version_info[0] == 2:
            raise err
        raise

    with open(path, 'r' + mode) as f:
        return module.load(f)


def destruct_path(path):
    if isinstance(path, tuple):
        filepath, jspath = path
    else:
        filepath = path
        jspath = None
    return filepath, jspath


def load_any(path):
    filepath, jspath = destruct_path(path)
    if jspath:
        from jsonpath_rw import parse
        jspath_expr = parse(jspath)
        root = load_any_file(filepath)
        matches = list(jspath_expr.find(root))
        if len(matches) == 0:
            raise LoaderError(
                'No object found at {} in {}'.format(jspath, filepath))
        elif len(matches) != 1:
            raise LoaderError(
                'Multiple objects found at {} in {}'.format(jspath, filepath))
        return matches[0].value
    else:
        return load_any_file(filepath)


def transforming_loader(files, transform, transform_to):
    module, mode = param_module('.' + transform_to)
    universal_newlines = mode != 'b'
    for path in files:
        with open(os.devnull) as devnull:
            proc = subprocess.Popen(
                transform.format(path),
                shell=True,
                stdout=subprocess.PIPE,
                stdin=devnull,
                universal_newlines=universal_newlines)
        yield module.load(proc.stdout)
        proc.wait()


def to_info_dict(dictpath):
    """
    Make an "info dict" which becomes a row of `.DictsDiff.info_df`.

    Parameters
    ----------
    dictpath : str or tuple
        It can be a string which is a filepath or a 2-tupe of filepath
        and a JSONPath.

    Returns
    -------
    info_dict : dict
        It has a key ``'path'`` with a string value and a key
        ``'filepath'`` wit has string value.

    """
    filepath, jspath = destruct_path(dictpath)
    if jspath:
        path = '{} {}'.format(filepath, jspath)
        return dict(path=path, filepath=filepath, jsonpath=jspath)
    else:
        return dict(path=filepath, filepath=filepath)


def diff_files(files, **kwds):
    files = list(files)
    value_dicts = list(map(load_any, files))
    info_dicts = list(map(to_info_dict, files))
    return DictsDiff(value_dicts, info_dicts, **kwds)


def diff_ndjson(stream, **kwds):
    import json
    return diff_dicts(map(json.loads, stream), **kwds)
