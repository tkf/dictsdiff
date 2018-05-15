import shutil

import pytest

from ..utils import get_terminal_size_stty


@pytest.mark.skipif(not hasattr(shutil, 'get_terminal_size'),
                    reason="require shutil.get_terminal_size")
@pytest.mark.xfail
def test_get_terminal_size_stty_with_shutil():
    size_shutil = shutil.get_terminal_size()
    size_stty = get_terminal_size_stty()
    assert size_shutil == size_stty


def test_get_terminal_size_stty_return_type():
    size_stty = get_terminal_size_stty()
    assert isinstance(size_stty, tuple)
    assert list(map(type, size_stty)) == [int, int]
