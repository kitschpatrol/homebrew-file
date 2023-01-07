import platform
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from . import brew_file


@pytest.fixture
def brew_info():
    helper = brew_file.BrewHelper({})
    info = brew_file.BrewInfo(
        helper=helper, file=Path(__file__).parent / "files" / "BrewfileTest"
    )
    return info


def test_get_dir(brew_info):
    assert brew_info.get_dir() == Path(f"{Path(__file__).parent}/files")


def test_check_file(brew_info):
    assert brew_info.check_file()
    info = brew_file.BrewInfo(helper=brew_info.helper, file=Path("not_exist"))
    assert not info.check_file()


def test_check_dir(brew_info):
    assert brew_info.check_dir()
    info = brew_file.BrewInfo(helper=brew_info.helper, file=Path("/not/exist"))
    assert not info.check_dir()


def test_clear_input(brew_info):
    brew_info.brew_input_opt.update({"abc": "abc"})
    brew_info.brew_input.extend(["abc", "efg"])
    brew_info.tap_input.extend(["abc", "efg"])
    brew_info.cask_input.extend(["abc", "efg"])
    brew_info.appstore_input.extend(["abc", "efg"])
    brew_info.main_input.extend(["abc", "efg"])
    brew_info.file_input.extend(["abc", "efg"])

    brew_info.before_input.extend(["abc", "efg"])
    brew_info.after_input.extend(["abc", "efg"])
    brew_info.cmd_input.extend(["abc", "efg"])
    brew_info.cask_args_input.update({"abc": "efg"})
    brew_info.clear_input()
    assert brew_info.brew_input_opt == {}
    assert brew_info.brew_input == []
    assert brew_info.tap_input == []
    assert brew_info.cask_input == []
    assert brew_info.appstore_input == []
    assert brew_info.main_input == []
    assert brew_info.file_input == []
    assert brew_info.before_input == []
    assert brew_info.after_input == []
    assert brew_info.cmd_input == []
    assert brew_info.cask_args_input == {}


def test_clear_list(brew_info):
    brew_info.brew_list_opt.update({"abc": "abc"})
    brew_info.brew_list.extend(["abc", "efg"])
    brew_info.brew_full_list.extend(["abc", "efg"])
    brew_info.tap_list.extend(["abc", "efg"])
    brew_info.cask_list.extend(["abc", "efg"])
    brew_info.appstore_list.extend(["abc", "efg"])
    brew_info.main_list.extend(["abc", "efg"])
    brew_info.file_list.extend(["abc", "efg"])

    # #brew_info.before_list = ['abc', 'efg']
    # #brew_info.after_list = ['abc', 'efg']
    # #brew_info.cmd_list = ['abc', 'efg']
    # #brew_info.cask_args_list = ['abc', 'efg']

    # brew_info.cask_noargs_list = ['abc', 'efg']

    brew_info.clear_list()
    assert brew_info.brew_list_opt == {}
    assert brew_info.brew_list == []
    assert brew_info.brew_full_list == []
    assert brew_info.tap_list == []
    assert brew_info.cask_list == []
    assert brew_info.appstore_list == []
    assert brew_info.main_list == []
    assert brew_info.file_list == []


def test_clear(brew_info):
    brew_info.brew_input_opt.update({"abc": "abc"})
    brew_info.brew_input.extend(["abc", "efg"])
    brew_info.tap_input.extend(["abc", "efg"])
    brew_info.cask_input.extend(["abc", "efg"])
    brew_info.appstore_input.extend(["abc", "efg"])
    brew_info.main_input.extend(["abc", "efg"])
    brew_info.file_input.extend(["abc", "efg"])
    brew_info.before_input.extend(["abc", "efg"])
    brew_info.after_input.extend(["abc", "efg"])
    brew_info.cmd_input.extend(["abc", "efg"])
    brew_info.cask_args_input.update({"abc": "efg"})

    brew_info.brew_list_opt.update({"abc": "abc"})
    brew_info.brew_list.extend(["abc", "efg"])
    brew_info.brew_full_list.extend(["abc", "efg"])
    brew_info.tap_list.extend(["abc", "efg"])
    brew_info.cask_list.extend(["abc", "efg"])
    brew_info.appstore_list.extend(["abc", "efg"])
    brew_info.main_list.extend(["abc", "efg"])
    brew_info.file_list.extend(["abc", "efg"])
    brew_info.clear()
    assert brew_info.brew_input_opt == {}
    assert brew_info.brew_input == []
    assert brew_info.brew_input == []
    assert brew_info.tap_input == []
    assert brew_info.cask_input == []
    assert brew_info.appstore_input == []
    assert brew_info.main_input == []
    assert brew_info.file_input == []
    assert brew_info.before_input == []
    assert brew_info.after_input == []
    assert brew_info.cmd_input == []
    assert brew_info.cask_args_input == {}
    assert brew_info.brew_list_opt == {}
    assert brew_info.brew_list == []
    assert brew_info.brew_full_list == []
    assert brew_info.tap_list == []
    assert brew_info.cask_list == []
    assert brew_info.appstore_list == []
    assert brew_info.main_list == []
    assert brew_info.file_list == []


def test_input_to_list(brew_info):
    brew_info.brew_input_opt.update({"brew_input": "opt"})
    brew_info.brew_input.extend(["brew"])
    brew_info.tap_input.extend(["tap"])
    brew_info.cask_input.extend(["cask"])
    brew_info.appstore_input.extend(["appstore"])
    brew_info.main_input.extend(["main"])
    brew_info.file_input.extend(["file"])

    brew_info.brew_list_opt.update({"abc": "abc"})
    brew_info.brew_list.extend(["abc", "efg"])
    brew_info.tap_list.extend(["abc", "efg"])
    brew_info.cask_list.extend(["abc", "efg"])
    brew_info.appstore_list.extend(["abc", "efg"])
    brew_info.main_list.extend(["abc", "efg"])
    brew_info.file_list.extend(["abc", "efg"])

    brew_info.input_to_list()

    assert brew_info.brew_input_opt == {"brew_input": "opt"}
    assert brew_info.brew_input == ["brew"]
    assert brew_info.tap_input == ["tap"]
    assert brew_info.cask_input == ["cask"]
    assert brew_info.appstore_input == ["appstore"]
    assert brew_info.main_input == ["main"]
    assert brew_info.file_input == ["file"]

    assert brew_info.brew_list_opt == {"brew_input": "opt"}
    assert brew_info.brew_list == ["brew"]
    assert brew_info.tap_list == ["tap"]
    assert brew_info.cask_list == ["cask"]
    assert brew_info.appstore_list == ["appstore"]
    assert brew_info.main_list == ["main"]
    assert brew_info.file_list == ["file"]


def test_sort(brew_info):
    brew_info.helper.opt["cask_repo"] = "homebrew/cask"
    brew_info.tap_list.extend(
        ["rcmdnk/file", "homebrew/cask", "homebrew/bundle", "homebrew/core"]
    )
    brew_info.appstore_list.extend(["111 ccc (2)", "222 aaa (1)", "bbb"])
    brew_info.sort()
    assert brew_info.tap_list == [
        "homebrew/core",
        "homebrew/cask",
        "homebrew/bundle",
        "rcmdnk/file",
    ]
    assert brew_info.appstore_list == ["222 aaa (1)", "bbb", "111 ccc (2)"]


def test_get(brew_info):
    brew_info.brew_input.extend(["brew"])
    brew_input = brew_info.get("brew_input")
    assert brew_input == ["brew"]
    brew_input.append("brew2")
    assert brew_info.brew_input == ["brew"]
    brew_input = brew_info.get("brew_input")
    assert brew_input == ["brew"]


def test_get_files(brew_info):
    files = brew_info.get_files()
    assert files == {
        "main": ["BrewfileMain"],
        "ext": [
            "BrewfileMain",
            "BrewfileExt",
            "BrewfileExt2",
            "BrewfileNotExist",
            "~/BrewfileHomeForTestingNotExists",
        ],
    }


def test_remove(brew_info):
    brew_info.brew_input.extend(["aaa", "bbb", "ccc"])
    brew_info.remove("brew_input", "bbb")
    assert brew_info.brew_input == ["aaa", "ccc"]
    brew_info.brew_input_opt.update({"aaa": "aaa", "bbb": "bbb", "ccc": "ccc"})
    brew_info.remove("brew_input_opt", "bbb")
    assert brew_info.brew_input_opt == {"aaa": "aaa", "ccc": "ccc"}


def test_set(brew_info):
    brew_info.brew_input.extend(["aaa", "bbb"])
    brew_info.set("brew_input", ["ccc"])
    assert brew_info.brew_input == ["ccc"]
    brew_info.brew_input_opt.update({"aaa": "aaa", "bbb": "bbb"})
    brew_info.set("brew_input_opt", {"ccc": "ccc"})
    assert brew_info.brew_input_opt == {"ccc": "ccc"}


def test_add(brew_info):
    brew_info.brew_input.extend(["aaa", "bbb"])
    brew_info.add("brew_input", ["aaa", "ccc"])
    assert brew_info.brew_input == ["aaa", "bbb", "ccc"]
    brew_info.brew_input_opt.update({"aaa": "aaa", "bbb": "bbb"})
    brew_info.add("brew_input_opt", {"aaa": "ddd", "ccc": "ccc"})
    assert brew_info.brew_input_opt == {
        "aaa": "ddd",
        "bbb": "bbb",
        "ccc": "ccc",
    }


def test_read(brew_info):
    brew_info.read()
    assert brew_info.brew_input_opt == {"python@3.10": "", "vim": " --HEAD"}
    assert brew_info.brew_input == ["python@3.10", "vim"]
    assert brew_info.tap_input == [
        "direct",
        "homebrew/core",
        "homebrew/cask",
        "rcmdnk/rcmdnkcask",
    ]
    assert brew_info.cask_input == ["iterm2", "font-migu1m"]
    assert brew_info.appstore_input == ["Keynote"]
    assert brew_info.main_input == ["BrewfileMain"]
    assert brew_info.file_input == [
        "BrewfileMain",
        "BrewfileExt",
        "BrewfileExt2",
        "BrewfileNotExist",
        "~/BrewfileHomeForTestingNotExists",
    ]
    assert brew_info.before_input == ["echo before"]
    assert brew_info.after_input == ["echo after"]
    assert brew_info.cmd_input == ["echo other commands"]


def test_get_tap_path(brew_info):
    tap_path = brew_info.get_tap_path("homebrew/core")
    assert tap_path.exists()


def test_get_tap_packs(brew_info):
    packs = brew_info.get_tap_packs("homebrew/core")
    assert "python@3.10" in packs


def test_get_tap_casks(brew_info):
    casks = brew_info.get_tap_casks("homebrew/cask")
    assert "iterm2" in casks


def test_get_leaves(brew_info):
    pass


def test_get_info(brew_info):
    info = brew_info.get_info("python@3.10")
    assert info["python@3.10"]["installed"][0]["used_options"] == []


def test_get_installed(brew_info):
    installed = brew_info.get_installed("python@3.10")
    assert installed["version"] == platform.python_version()


def test_get_option(brew_info):
    opt = brew_info.get_option("python@3.10")
    assert opt == ""


def test_convert_option(brew_info):
    brew_info.helper.opt["form"] = "file"
    opt = brew_info.convert_option("--HEAD --test")
    assert opt == "--HEAD --test"
    brew_info.helper.opt["form"] = "bundle"
    opt = brew_info.convert_option(" --HEAD --test")
    assert opt == ", args: ['HEAD', 'test']"


def test_packout(brew_info):
    brew_info.helper.opt["form"] = "file"
    assert brew_info.packout("package") == "package"
    brew_info.helper.opt["form"] = "bundle"
    assert brew_info.packout("package") == "'package'"


def test_mas_pack(brew_info):
    brew_info.helper.opt["form"] = "file"
    assert (
        brew_info.mas_pack("409183694   Keynote  (12.2.1)")
        == "409183694   Keynote  (12.2.1)"
    )
    brew_info.helper.opt["form"] = "bundle"
    assert (
        brew_info.mas_pack("409183694   Keynote  (12.2.1)")
        == "'Keynote (12.2.1)', id: 409183694"
    )


# Ignore DeprecationWarning to allow \$
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_write(brew_info):
    default_file = brew_info.file
    with NamedTemporaryFile() as f:
        brew_info.helper.opt["caskonly"] = False
        brew_info.helper.opt["appstore"] = -1
        brew_info.helper.opt["verbose"] = 1
        brew_info.helper.opt["form"] = None
        brew_info.helper.opt["cask_repo"] = "homebrew/cask"
        brew_info.read()
        brew_info.input_to_list()
        brew_info.file = Path(f.name)
        print("here brew_info.file 0", brew_info.file)
        brew_info.write()
        print("here f.name", f.name)
        print("here brew_info.file 1", brew_info.file)
        with (open(default_file) as f1, open(f.name) as f2):
            assert f1.read() == f2.read()
        brew_info.helper.opt["form"] = "bundle"
        brew_info.write()
        with open(f.name) as f2:
            assert (
                f2.read()
                == """# Before commands
#before echo before

# tap repositories and their packages

tap 'homebrew/core'

tap 'homebrew/cask'

tap 'rcmdnk/rcmdnkcask'

# App Store applications
mas '', id: Keynote

# Main file
#main 'BrewfileMain'

# Additional files
#file 'BrewfileExt'
#file 'BrewfileExt2'
#file 'BrewfileNotExist'
#file '~/BrewfileHomeForTestingNotExists'

# Other commands
#echo other commands

# After commands
#after echo after
"""
            )

        brew_info.helper.opt["form"] = "cmd"
        brew_info.write()
        with open(f.name) as f2:
            assert (
                f2.read()
                == """#!/usr/bin/env bash

#BREWFILE_IGNORE
if ! which brew >& /dev/null;then
  brew_installed=0
  echo Homebrew is not installed!
  echo Install now...
  echo /bin/bash -c \\\"\\$\\(curl -fsSL https://raw.githubusercontent.com/Homebrew/ install/master/install.sh\\)\\\"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/ install/master/install.sh)"
  echo
fi
#BREWFILE_ENDIGNORE

# Before commands
echo before

# tap repositories and their packages

brew tap homebrew/core

brew tap homebrew/cask

brew tap rcmdnk/rcmdnkcask

# App Store applications
mas install Keynote

# Main file
#main BrewfileMain

# Additional files
#file BrewfileExt
#file BrewfileExt2
#file BrewfileNotExist
#file ~/BrewfileHomeForTestingNotExists

# Other commands
echo other commands

# After commands
echo after
"""
            )
