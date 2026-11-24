import stat
import sys
from pathlib import Path

import pytest

from app import paths
from app.config import Config, Source, StageConfig, config_path, from_dict, load, save


def test_the_settings_survive_a_restart(tmp_path):
    config = Config(
        token="cup",
        title="Cup",
        publish_section=4,
        final=True,
        place_everybody=True,
        stages=[
            StageConfig("Sprint", Source.SITE, token="stage", section=3),
            StageConfig("Jump", Source.SHEET, link="https://docs.test/1", rule="x"),
            StageConfig("Tries", leader_laps_only=False),
        ],
    )
    path = tmp_path / "data" / "config.json"
    save(config, path)
    assert load(path) == (config, "")


def test_a_save_a_full_disk_cuts_short_keeps_the_old_file_whole(tmp_path, monkeypatch):
    path = tmp_path / "config.json"
    save(Config(token="cup"), path)
    real = Path.write_text

    def full_disk(self, text, *args, **kwargs):
        real(self, text[:20], *args, **kwargs)
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(Path, "write_text", full_disk)
    with pytest.raises(OSError, match="No space left"):
        save(Config(token="other"), path)
    monkeypatch.undo()
    assert load(path)[0].token == "cup"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions")
def test_a_save_keeps_the_files_own_permissions_and_a_new_file_is_its_owners(tmp_path):
    # The file holds the upload tokens: a referee's chmod 600 must survive a save.
    path = tmp_path / "config.json"
    stale = tmp_path / "config.json.tmp"  # a save cut short left it open to all
    stale.write_text("{")
    stale.chmod(0o644)
    save(Config(token="cup"), path)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    path.chmod(0o640)
    save(Config(token="other"), path)
    assert stat.S_IMODE(path.stat().st_mode) == 0o640


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX links")
def test_a_linked_settings_file_is_saved_through_its_link(tmp_path):
    # A file kept in a folder two machines sync: the link must not become a copy.
    real = tmp_path / "synced" / "config.json"
    real.parent.mkdir()
    save(Config(token="cup"), real)
    link = tmp_path / "config.json"
    link.symlink_to(real)
    save(Config(token="other"), link)
    assert link.is_symlink()
    assert load(real)[0].token == "other"


def test_no_file_gives_the_defaults_and_says_nothing(tmp_path):
    assert load(tmp_path / "missing.json") == (Config(), "")


@pytest.mark.parametrize(
    "broken",
    [
        b'{"token": "cup",}',  # a comma left behind by hand
        '{"title": "\u041a\u0443\u0431\u043e\u043a"}'.encode("cp1251"),  # ANSI
    ],
)
def test_a_file_that_cannot_be_read_is_kept_aside_and_said(tmp_path, broken):
    # The next save, closing the window too, must not write the defaults over it.
    path = tmp_path / "config.json"
    path.write_bytes(broken)
    config, said = load(path)
    assert config == Config()
    assert said.startswith("ERROR: settings not read (")
    assert said.endswith("): kept as config.json.unreadable")
    assert not path.exists()
    assert (tmp_path / "config.json.unreadable").read_bytes() == broken


def test_a_file_that_cannot_be_kept_aside_either_is_said(tmp_path, monkeypatch):
    def held(self, target):
        raise PermissionError(13, "Permission denied")

    path = tmp_path / "config.json"
    path.write_text("{not json")
    monkeypatch.setattr(Path, "replace", held)
    config, said = load(path)
    assert config == Config()
    assert "nor kept aside ([Errno 13] Permission denied)" in said
    assert said.endswith("nothing is saved over it; restart once it can be read")


def test_a_file_with_a_byte_order_mark_keeps_its_settings(tmp_path):
    path = tmp_path / "config.json"
    save(Config(token="cup", title="Spring cup"), path)
    path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())  # as Notepad saves it
    config, said = load(path)
    assert (config.token, config.title, said) == ("cup", "Spring cup", "")


@pytest.mark.parametrize("data", [[], "text", None])
def test_settings_that_are_not_an_object_give_the_defaults(data):
    assert from_dict(data) == Config()


def test_a_new_cup_starts_with_one_stage():
    assert Config().stages == [StageConfig()]
    assert from_dict({"stages": []}).stages == [StageConfig()]
    assert from_dict({"stages": "none"}).stages == [StageConfig()]


def test_a_setting_of_the_wrong_shape_falls_back_to_its_default():
    config = from_dict(
        {
            "token": 7,
            "publish_section": True,
            "final": "yes",
            "place_everybody": 1,
            "stages": [
                {
                    "name": "A",
                    "source": "ftp",
                    "section": 0,
                    "link": 5,
                    "leader_laps_only": "no",
                },
                "not a stage",
            ],
        }
    )
    assert (config.token, config.publish_section, config.final) == ("", 2, False)
    assert config.place_everybody is False
    assert config.stages == [StageConfig(name="A"), StageConfig()]


def test_the_settings_file_is_kept_in_data_next_to_the_app(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert config_path() == tmp_path / "data" / "config.json"


def test_a_built_app_keeps_its_data_next_to_itself(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "Cup"))
    assert paths.base_dir() == tmp_path
    bundle = tmp_path / "Cup.app" / "Contents" / "MacOS" / "Cup"
    monkeypatch.setattr(sys, "executable", str(bundle))
    assert paths.base_dir() == tmp_path
