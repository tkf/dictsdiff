from .core import DictsDiff, diff_dicts


def param_module(path):
    if path.lower().endswith(('.yaml', '.yml')):
        import yaml
        return yaml
    elif path.lower().endswith('.json'):
        import json
        return json
    elif path.lower().endswith('.pickle', '.pkl'):
        try:
            import cPickle as pickle
        except:
            import pickle
        return pickle
    else:
        raise ValueError('data format of {!r} is not supported'.format(path))


def load_any_file(path):
    """
    Load data from given path; data format is determined by file extension
    """
    loader = param_module(path).load
    with open(path) as f:
        return loader(f)


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
            raise RuntimeError('No object found at {} in {}'
                               .format(jspath, filepath))
        elif len(matches) != 1:
            raise RuntimeError('Multiple objects found at {} in {}'
                               .format(jspath, filepath))
        return matches[0].value
    else:
        return load_any_file(path)


def to_info_dict(path):
    filepath, jspath = destruct_path(path)
    if jspath:
        path = '{} {}'.format(filepath, jspath)
        return dict(path=path, filepath=filepath, jsonpath=jspath)
    else:
        return dict(path=path)


def diff_files(files, **kwds):
    files = list(files)
    value_dicts = list(map(load_any, files))
    info_dicts = list(map(to_info_dict, files))
    return DictsDiff(value_dicts, info_dicts, **kwds)


def diff_ndjson(stream, **kwds):
    import json
    return diff_dicts(map(json.loads, stream), **kwds)
