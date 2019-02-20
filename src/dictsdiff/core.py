import numpy
import pandas


class DictsDiffError(Exception):
    pass


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
    force_tuple_columns(df)
    return df


def force_tuple_columns(df):
    if len(df.columns) > 0 and not isinstance(df.columns[0], tuple):
        # Workaround for the bug in pandas:
        # https://github.com/pandas-dev/pandas/issues/16769
        newcolumns = [c if isinstance(c, tuple) else (c,) for c in df.columns]
        dummy = object()
        df[dummy] = pandas.Categorical(0)
        df.columns = newcolumns + [dummy]
        del df[dummy]


def different_keys(df, rtol=0, atol=0):
    if len(df) <= 1:
        return
    for key, dtype in zip(df.columns, df.dtypes):
        column = df[key].values  # to 1D numpy array
        if (rtol or atol) and numpy.issubdtype(dtype, numpy.floating):
            if not numpy.allclose(column[0], column[1:], rtol=rtol, atol=atol):
                yield key
        elif dtype == object:
            # Since "column[0] == column[1:]" does not work for object
            # array, it is handled explicitly here.
            first = column[0]
            if not all(first == c for c in column[1:]):
                yield key
        elif not (column[0] == column[1:]).all():
            yield key


def pretty_column_keys(columns):
    return list(map('.'.join, columns))


class DictsDiff(object):

    def __init__(self, value_dicts, info_dicts, info_keys=[], **kwds):
        self.value_df = dicts_to_dataframe(value_dicts)
        self.info_df = dicts_to_dataframe(info_dicts)
        self._move_info_values(info_keys)
        force_tuple_columns(self.info_df)
        self.info_keys = info_keys
        self.keys = sorted(different_keys(self.value_df, **kwds))
        self.diff_df = pandas.concat(
            [self.value_df[self.keys], self.info_df],
            axis=1,
            keys=['value', 'info'],
        )

    def _move_info_values(self, info_keys):
        for key in info_keys:
            try:
                self.info_df[key] = self.value_df.pop(key)
            except KeyError:
                pass

    def pretty_diff(self):
        df = self.diff_df.copy()

        df_has_path = ('info', ('path',)) in df
        if self.info_keys:
            df = df.set_index([('info', key) for key in self.info_keys])
        elif df_has_path:
            paths = df['info', ('path',)]

        try:
            df = df.loc[:, ("value", slice(None))]
        except KeyError:
            assert not self.keys
            # This seems to be pandas' bug...
            df = pandas.DataFrame(index=df.index)
        else:
            df.columns = df.columns.droplevel()

        if self.info_keys:
            # Throw away ('info', ...) part and then prettify the
            # index names.  Note that n[0] below is always 'info':
            df.index.names = pretty_column_keys(n[1] for n in df.index.names)
        elif df_has_path:
            df.index = paths
            df.index.name = 'path'

        df.columns = pretty_column_keys(df.columns)
        return df


def diff_dicts(value_dicts, **kwds):
    value_dicts = list(value_dicts)
    info_dicts = [{}] * len(value_dicts)
    return DictsDiff(value_dicts, info_dicts, **kwds)
