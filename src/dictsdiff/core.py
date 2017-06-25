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
    df = pandas.DataFrame.from_dict([dict(iteritemsdeep(d)) for d in dicts])
    if len(df.columns) > 0 and not isinstance(df.columns[0], tuple):
        # Workaround for the bug in pandas:
        # https://github.com/pandas-dev/pandas/issues/16769
        newcolumns = [c if isinstance(c, tuple) else (c,) for c in df.columns]
        dummy = object()
        df[dummy] = pandas.Categorical(0)
        df.columns = newcolumns + [dummy]
        del df[dummy]

    # Convert columns with lists to tuples, since .unique() does not
    # work with lists (it requires hash-able values):
    for key, dtype in zip(df.columns, df.dtypes):
        if dtype == object and (df[key].apply(type) == list).any():
            df[key] = df[key].apply(tuple)
    return df


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
