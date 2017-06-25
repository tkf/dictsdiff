import pytest

from ..core import diff_dicts


@pytest.mark.parametrize('value_dicts, diff_keys', [
    ([dict(a=1)] * 2, []),
    ([dict(a=1), dict(a=2)], ['a']),
    ([dict(a=1), dict(b=1)], ['a', 'b']),
])
def test_diff_flat_keys(value_dicts, diff_keys):
    dd = diff_dicts(value_dicts)
    assert dd.keys == sorted((k,) for k in diff_keys)
