import pandas


def iteritemsdeep(dct):
    """
    Works like ``dict.iteritems`` but iterate over all descendant items

    >>> dct = dict(a=1, b=2, c=dict(d=3, e=4))
    >>> sorted(iteritemsdeep(dct))
    [(('a',), 1), (('b',), 2), (('c', 'd'), 3), (('c', 'e'), 4)]

    """
    for (key, val) in dct.items():
        if isinstance(val, dict):
            for (key_child, val_child) in iteritemsdeep(val):
                yield ((key,) + key_child, val_child)
        else:
            yield ((key,), val)


def dicts_to_dataframe(dicts):
    return pandas.DataFrame.from_dict([dict(iteritemsdeep(d)) for d in dicts])


def different_keys(df):
    for key in df.columns:
        if len(df[key].unique()) != 1:
            yield key


class DictsDiff(object):

    def __init__(self, value_dicts, info_dicts):
        self.value_df = dicts_to_dataframe(value_dicts)
        self.info_df = dicts_to_dataframe(info_dicts)
        self.keys = sorted(different_keys(self.value_df))
        self.diff_df = pandas.concat(
            [self.value_df[self.keys], self.info_df],
            axis=1,
            keys=['value', 'info'],
        )


def diff_dicts(value_dicts):
    value_dicts = list(value_dicts)
    info_dicts = [{}] * len(value_dicts)
    return DictsDiff(value_dicts, info_dicts)
