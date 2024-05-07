import pytest

from mkrp.modules.gitignore import get_gitignore


def test_get_gitignore():
    gitignore = get_gitignore(['python'])
    assert 'poetry.lock' in gitignore


def test_get_gitignore_invalid():
    with pytest.raises(ValueError):
        get_gitignore(['python', 'poetry'])
