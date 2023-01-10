import pytest

from .brew_file import StrRe


@pytest.mark.parametrize(
    "var, pattern, ret",
    [
        ("abc efg", "^ *abc ", True),
        ("  abc efg", "^ *abc ", True),
        ("  abcefg", "^ *abc ", False),
        ("abc efg", "^ *abc$", False),
        ("abc", "^ *abc$", True),
        ("abc.xyz", "\\.xyz", True),
        (" abc.xyz", "\\.xyz", True),
    ],
)
def test_str_re(var, pattern, ret):
    assert (StrRe(var) == pattern) == ret
