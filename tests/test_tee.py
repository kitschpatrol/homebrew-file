import sys
from tempfile import TemporaryDirectory

from . import brew_file


def test_tee(capsys):
    with TemporaryDirectory() as tmpdir:
        out = brew_file.Tee(f"{tmpdir}/out1")
        out.write("test\n")
        out.writeln("test_ln")
        out.flush()
        out.close()
        with open(f"{tmpdir}/out1") as f:
            assert f.read() == "test\ntest_ln\n"
        sys.stdout.flush()
    captured = capsys.readouterr()
    assert captured.out == "test\ntest_ln\n"
    assert captured.err == ""


def test_tee_out2_file(capsys):
    with TemporaryDirectory() as tmpdir:
        out = brew_file.Tee(f"{tmpdir}/out1", f"{tmpdir}/out2")
        out.write("test\n")
        out.writeln("test_ln")
        out.flush()
        out.close()
        with open(f"{tmpdir}/out1") as f:
            assert f.read() == "test\ntest_ln\n"
        with open(f"{tmpdir}/out2") as f:
            assert f.read() == "test\ntest_ln\n"
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_tee_no_out2(capsys):
    with TemporaryDirectory() as tmpdir:
        out = brew_file.Tee(f"{tmpdir}/out1", use2=False)
        out.write("test\n")
        out.writeln("test_ln")
        out.flush()
        out.close()
        with open(f"{tmpdir}/out1") as f:
            assert f.read() == "test\ntest_ln\n"
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
