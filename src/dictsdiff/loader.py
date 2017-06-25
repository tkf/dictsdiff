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


def load_any(path):
    """
    Load data from given path; data format is determined by file extension
    """
    loader = param_module(path).load
    with open(path) as f:
        return loader(f)


def diff_files(files, **kwds):
    files = list(files)
    value_dicts = list(map(load_any, files))
    info_dicts = [dict(path=path) for path in files]
    return DictsDiff(value_dicts, info_dicts, **kwds)


def diff_ndjson(stream, **kwds):
    import json
    return diff_dicts(map(json.loads, stream), **kwds)
