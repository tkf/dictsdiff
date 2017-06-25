import pytest

from ..core import diff_dicts


@pytest.mark.parametrize('value_dicts, diff_keys', [
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
])
def test_float_diff_with_tol(value_dicts, diff_keys, rtol, atol):
    dd = diff_dicts(value_dicts, rtol=rtol, atol=atol)
    assert dd.keys == sorted((k,) for k in diff_keys)
