import io
import os
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from . import brew_file


@pytest.fixture
def bf():
    obj = brew_file.BrewFile({})
    return obj


def test_debug_banner(bf, capsys):
    bf.debug_banner()
    captured = capsys.readouterr()
    assert captured.out == ""
    bf.opt["dryrun"] = True
    bf.debug_banner()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "\n##################\n# This is dry run.\n##################\n\n"
    )


def test_parse_env_opts(bf):
    os.environ["TEST_OPT"] = "--opt2=3 --opt3 opt4=4"
    opts = bf.parse_env_opts("test_opt", {"--opt1": "1", "--opt2": "2"})
    assert opts == {"--opt1": "1", "--opt2": "3", "--opt3": "", "opt4": "4"}


def test_set_args(bf):
    bf.opt["appstore"] = 1
    bf.opt["no_appstore"] = 1
    bf.set_args(a="1", verbose="1")
    assert isinstance(bf.opt["a"], str)
    assert isinstance(bf.opt["verbose"], int)
    assert bf.opt["appstore"] == 1
    bf.opt["appstore"] = -1
    bf.opt["no_appstore"] = False
    bf.set_args()
    assert bf.opt["appstore"] == 0
    bf.opt["appstore"] = 1
    bf.opt["no_appstore"] = False
    bf.set_args()
    assert bf.opt["appstore"] == 1


@pytest.mark.parametrize(
    "input_value, ret, out",
    [
        ("y\n", True, "Question? [y/n]: "),
        ("Y\n", True, "Question? [y/n]: "),
        ("yes\n", True, "Question? [y/n]: "),
        ("YES\n", True, "Question? [y/n]: "),
        ("Yes\n", True, "Question? [y/n]: "),
        ("n\n", False, "Question? [y/n]: "),
        ("N\n", False, "Question? [y/n]: "),
        ("no\n", False, "Question? [y/n]: "),
        ("NO\n", False, "Question? [y/n]: "),
        ("No\n", False, "Question? [y/n]: "),
        (
            "a\nb\ny\n",
            True,
            "Question? [y/n]: Answer with yes (y) or no (n): Answer with yes (y) or no (n): ",
        ),
    ],
)
def test_ask_yn(bf, capsys, monkeypatch, input_value, ret, out):
    monkeypatch.setattr("sys.stdin", io.StringIO(input_value))
    assert bf.ask_yn("Question?") == ret
    captured = capsys.readouterr()
    assert captured.out == out


def test_verbose(bf):
    bf.opt["verbose"] = 1
    assert bf.verbose() == 1
    del bf.opt["verbose"]
    assert bf.verbose() == 10


def test_proc(bf):
    pass


def test_remove(bf, capsys):
    with TemporaryDirectory() as tmpdir:
        file = Path(Path(tmpdir) / "testfile")
        file.touch()
        bf.remove(str(file))
        directory = Path(Path(tmpdir) / "testdir")
        directory.mkdir()
        file = Path(directory / "testfile")
        file.touch()
        bf.remove(str(directory))
        bf.remove(f"{tmpdir}/notexist")
        captured = capsys.readouterr()
        assert (
            captured.out
            == f"[WARNING]: Tried to remove non usual file/directory: {tmpdir}/notexist\n"
        )


def test_brew_val(bf):
    prefix = "/".join(bf.proc("which brew")[1][0].split("/")[:-2])
    assert bf.brew_val("prefix") == prefix


def test_read_all(bf):
    bf.opt["input"] = f"{Path(__file__).parent}/files/BrewfileTest"
    bf.read_all()
    print(bf.brewinfo_main)
    print(bf.brewinfo_ext)
    print(bf.get("brew_input"))
    print(bf.get("brew_input_opt"))
    print(bf.get("tap_input"))
    print(bf.get("cask_input"))
    print(bf.get("appstore_input"))
    print(bf.get("main_input"))
    print(bf.get("file_input"))
    print(bf.get("before_input"))
    print(bf.get("after_input"))
    print(bf.get("cmd_input"))


def test_read(bf):
    helper = brew_file.BrewHelper({})

    bf.brewinfo_ext = []
    file = Path(f"{Path(__file__).parent}/files/BrewfileMain")
    brewinfo = brew_file.BrewInfo(helper=helper, file=file)
    ret = bf.read(brewinfo, True)
    assert ret.file == file

    bf.brewinfo_ext = []
    file = Path(f"{Path(__file__).parent}/files/BrewfileMain")
    brewinfo = brew_file.BrewInfo(helper=helper, file=file)
    ret = bf.read(brewinfo, False)
    assert ret is None

    bf.brewinfo_ext = []
    file = Path(f"{Path(__file__).parent}/files/BrewfileTest")
    brewinfo = brew_file.BrewInfo(helper=helper, file=file)
    ret = bf.read(brewinfo, True)
    file = Path(f"{Path(__file__).parent}/files/BrewfileMain")
    assert ret.file == file
    files = [
        Path(f"{Path(__file__).parent}/files/BrewfileMain"),
        Path(f"{Path(__file__).parent}/files/BrewfileExt"),
        Path(f"{Path(__file__).parent}/files/BrewfileExt2"),
        Path(f"{Path(__file__).parent}/files/BrewfileExt3"),
        Path(f"{Path(__file__).parent}/files/BrewfileNotExist"),
        Path(Path("~/BrewfileHomeForTestingNotExists").expanduser()),
    ]
    for i, f in zip(bf.brewinfo_ext, files):
        assert i.file == f

    # Absolute path check
    with NamedTemporaryFile() as f1, NamedTemporaryFile() as f2, NamedTemporaryFile() as f3:
        with open(f1.name, "w") as f:
            f.write(f"main {f2.name}")
        with open(f2.name, "w") as f:
            f.write(f"main {f3.name}")

        bf.brewinfo_ext = []
        brewinfo = brew_file.BrewInfo(helper=helper, file=Path(f1.name))
        ret = bf.read(brewinfo, True)
        assert ret.file == Path(f3.name)


def test_list_to_main(bf):
    pass


def test_input_to_list(bf):
    pass


def test_write(bf):
    pass


def test_get(bf):
    pass


def test_remove_pack(bf):
    pass


def test_repo_name(bf):
    bf.opt["repo"] = "git@github.com:abc/def.git"
    assert bf.repo_name() == "def"
    bf.opt["repo"] = "https://github.com/abc/def.git"
    assert bf.repo_name() == "def"


def test_user_name(bf):
    bf.opt["repo"] = "git@github.com:abc/def.git"
    assert bf.user_name() == "abc"
    bf.opt["repo"] = "https://github.com/abc/def.git"
    assert bf.user_name() == "abc"


def test_input_dir(bf):
    pass


def test_input_file(bf):
    pass


def test_repo_file(bf):
    pass


def test_init_repo(bf):
    pass


def test_clone_repo(bf):
    pass


def test_check_github_repo(bf):
    pass


def test_check_local_repo(bf):
    pass


def test_check_repo(bf):
    pass


def test_check_gitconfig(bf):
    pass


def test_repomgr(bf):
    pass


def test_brew_cmd(bf):
    pass


def test_check_brwe_cmd(bf):
    pass


def test_check_mas_cmd(bf):
    pass


def test_get_appstore_list(bf):
    pass


def test_get_cask_list(bf):
    pass


def test_get_list(bf):
    pass


def test_clean_list(bf):
    pass


def test_input_backup(bf):
    pass


def test_set_brewfile_repo(bf):
    pass


def test_set_brewfile_local(bf):
    pass


def test_initialize(bf):
    pass


def test_initialize_write(bf):
    pass


def test_check_input_file(bf):
    pass


def test_get_files(bf):
    pass


def test_edit_brewfile(bf):
    pass


def test_cat_brewfile(bf):
    pass


def test_clean_non_request(bf):
    pass


def test_cleanup(bf):
    pass


def test_install(bf):
    pass


def test_find_app(bf):
    pass


def test_find_brew_app(bf):
    pass


def test_check_cask(bf):
    pass


def test_make_pack_deps(bf):
    pass


def test_my_test(bf, capsys):
    bf.my_test()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "test\ntest\n[WARNING]: Tried to remove non usual file/directory: aaa\nread input: 0\nread input cleared: 0\n{'test_pack': 'test opt', 'test_pack2': 'test opt2'}\n"
    )


def test_execute(bf):
    pass
