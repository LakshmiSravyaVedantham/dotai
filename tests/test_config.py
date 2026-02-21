"""Tests for dotai.config module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotai.config import (
    add_rule,
    create_default_config,
    detect_project_info,
    get_config_path,
    read_config,
    remove_rule,
    write_config,
)


def test_get_config_path_default(tmp_path: Path) -> None:
    path = get_config_path(tmp_path)
    assert path == tmp_path / ".ai" / "config.yml"


def test_get_config_path_custom() -> None:
    custom = Path("/some/project")
    path = get_config_path(custom)
    assert path == custom / ".ai" / "config.yml"


def test_write_and_read_config(tmp_path: Path) -> None:
    config_path = get_config_path(tmp_path)
    data = {"version": 1, "rules": ["test rule"]}
    write_config(config_path, data)
    assert config_path.exists()
    loaded = read_config(config_path)
    assert loaded["version"] == 1
    assert loaded["rules"] == ["test rule"]


def test_read_config_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.yml"
    assert read_config(path) == {}


def test_read_config_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "bad.yml"
    path.write_text("just a string", encoding="utf-8")
    assert read_config(path) == {}


def test_create_default_config() -> None:
    config = create_default_config()
    assert config["version"] == 1
    assert "project" in config
    assert "rules" in config
    assert isinstance(config["rules"], list)
    assert len(config["rules"]) > 0
    assert "context" in config
    assert "style" in config
    assert "testing" in config


def test_add_rule(sample_config: dict[str, Any]) -> None:
    add_rule(sample_config, "New rule")
    assert "New rule" in sample_config["rules"]


def test_add_rule_no_duplicates(sample_config: dict[str, Any]) -> None:
    original_len = len(sample_config["rules"])
    add_rule(sample_config, sample_config["rules"][0])
    assert len(sample_config["rules"]) == original_len


def test_add_rule_creates_list() -> None:
    config: dict[str, Any] = {}
    add_rule(config, "First rule")
    assert config["rules"] == ["First rule"]


def test_remove_rule(sample_config: dict[str, Any]) -> None:
    rule = sample_config["rules"][0]
    assert remove_rule(sample_config, rule) is True
    assert rule not in sample_config["rules"]


def test_remove_rule_not_found(sample_config: dict[str, Any]) -> None:
    assert remove_rule(sample_config, "nonexistent") is False


def test_detect_python_project(python_project: Path) -> None:
    info = detect_project_info(python_project)
    assert info["language"] == "python"
    assert info["name"] == "testproj"
    assert info["linting"] == "ruff"
    assert info["testing"] == "pytest"


def test_detect_js_project(js_project: Path) -> None:
    info = detect_project_info(js_project)
    assert info["language"] == "javascript"
    assert info["framework"] == "react"
    assert info["name"] == "testapp"


def test_detect_go_project(tmp_path: Path) -> None:
    (tmp_path / "go.mod").write_text("module example.com/test", encoding="utf-8")
    info = detect_project_info(tmp_path)
    assert info["language"] == "go"


def test_detect_rust_project(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text('[package]\nname = "test"', encoding="utf-8")
    info = detect_project_info(tmp_path)
    assert info["language"] == "rust"


def test_detect_unknown_project(tmp_path: Path) -> None:
    info = detect_project_info(tmp_path)
    assert "language" not in info
    assert info["name"] == tmp_path.name


def test_detect_django_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "djapp"', encoding="utf-8"
    )
    (tmp_path / "manage.py").write_text("#!/usr/bin/env python", encoding="utf-8")
    info = detect_project_info(tmp_path)
    assert info["framework"] == "django"


def test_detect_fastapi_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "api"\ndependencies = ["fastapi"]',
        encoding="utf-8",
    )
    info = detect_project_info(tmp_path)
    assert info["framework"] == "fastapi"
