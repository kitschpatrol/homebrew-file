import sys

from .brew_file import __date__, __prog__, __version__, main


def test_version(capsys):
    sys.argv = ["brew-file", "--version"]
    ret = main()
    captured = capsys.readouterr()
    assert ret == 0
    assert "Homebrew" in captured.out
    assert f"{__prog__} {__version__} {__date__}" in captured.out
