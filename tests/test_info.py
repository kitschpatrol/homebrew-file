import tomli
from .brew_file import __version__


def test_version():
    with open("pyproject.toml", 'rb') as f:
        version = tomli.load(f)["tool"]["poetry"]["version"]
    assert version == __version__
