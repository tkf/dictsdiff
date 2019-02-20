import pytest

from ..core import DictsDiff, diff_dicts


@pytest.mark.parametrize('value_dicts, diff_keys', [
    ([dict(a=1)], []),
    ([dict(a=1)] * 2, []),
    ([dict(a=1), dict(a=2)], ['a']),
    ([dict(a=1), dict(b=1)], ['a', 'b']),
    ([dict(a=[1]), dict(a=[1])], []),
    ([dict(a=[1]), dict(a=[2])], ['a']),
])
def test_diff_flat_keys(value_dicts, diff_keys):
    dd = diff_dicts(value_dicts)
    assert dd.keys == sorted((k,) for k in diff_keys)


@pytest.mark.parametrize('value_dicts, diff_keys, rtol, atol', [
    ([dict(a=1.0)] * 2, [], 0, 0),
    ([dict(a=1.0), dict(a=0.999)], ['a'], 0, 0),
    ([dict(a=1.0), dict(a=0.999)], [], 1e-2, 0),
    ([dict(a=1.0), dict(a=0.999)], [], 0, 1e-2),
    ([dict(a=1.0), dict(a=0.999)], ['a'], 1e-6, 0),
    ([dict(a=1.0), dict(a=0.999)], ['a'], 0, 1e-6),
])
def test_float_diff_with_tol(value_dicts, diff_keys, rtol, atol):
    dd = diff_dicts(value_dicts, rtol=rtol, atol=atol)
    assert dd.keys == sorted((k,) for k in diff_keys)


def test_info_keys_with_nonempty_info_dicts():
    dd = DictsDiff(
        [dict(a=dict(b=111, c=0)), dict(a=dict(b=222, c=1))],
        [dict(path='x'), dict(path='y')],
        info_keys=[('a', 'b')],
    )
    df = dd.pretty_diff()
    assert list(df.columns) == ['a.c']
    assert list(df.index.names) == ['a.b']
    assert list(df.index) == [111, 222]


def test_info_keys_with_empty_info_dicts():
    dd = diff_dicts(
        [dict(a=dict(b=111, c=0)), dict(a=dict(b=222, c=1))],
        info_keys=[('a', 'b')],
    )
    df = dd.pretty_diff()
    assert list(df.columns) == ['a.c']
    assert list(df.index.names) == ['a.b']
    assert list(df.index) == [111, 222]


def test_info_keys_with_nonexistent_info_keys():
    dd = diff_dicts(
        [dict(a=dict(b=111, c=0)), dict(a=dict(b=222, c=1))],
        info_keys=[('spam', 'egg')],
    )
    return dd  # TODO: merge it with below
#
# ...or maybe this shouldn't be allowed?  If I were to go that path, I
# shouldn't ignore `KeyError` in `DictsDiff._move_info_values`.


@pytest.mark.xfail(raises=KeyError)
def test_info_keys_with_nonexistent_info_keys_xfail():
    dd = test_info_keys_with_nonexistent_info_keys()
    df = dd.pretty_diff()
    assert list(df.columns) == ['a.b', 'a.c']
    assert list(df.index.names) == []


def test_no_diff():
    d1 = dict(a=dict(b=111, c=0))
    dd = diff_dicts([d1, d1, d1])
    df = dd.pretty_diff()
    assert len(df.columns) == 0
