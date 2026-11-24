import sys

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
    assert load(path) == config


def test_no_file_or_a_broken_one_gives_the_defaults(tmp_path):
    assert load(tmp_path / "missing.json") == Config()
    broken = tmp_path / "broken.json"
    broken.write_text("{not json")
    assert load(broken) == Config()


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
