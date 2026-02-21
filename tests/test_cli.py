"""Tests for dotai CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from dotai.cli import app
from dotai.config import get_config_path, write_config

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "dotai" in result.output


def test_no_args() -> None:
    result = runner.invoke(app)
    # no_args_is_help=True causes exit code 0 (typer shows help)
    assert result.exit_code in (0, 2)


def test_init(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Created" in result.output
    assert (tmp_path / ".ai" / "config.yml").exists()


def test_init_with_python_project(python_project: Path) -> None:
    result = runner.invoke(app, ["init", "--dir", str(python_project)])
    assert result.exit_code == 0
    assert "python" in result.output.lower() or "Created" in result.output


def test_sync(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["sync", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Synced" in result.output
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".cursorrules").exists()
    assert (tmp_path / ".windsurfrules").exists()
    assert (tmp_path / ".clinerules").exists()
    assert (tmp_path / ".aider.conf.yml").exists()
    assert (tmp_path / ".github" / "copilot-instructions.md").exists()


def test_sync_single_tool(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["sync", "--dir", str(tmp_path), "--tool", "claude"])
    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").exists()
    # Others should NOT exist
    assert not (tmp_path / ".cursorrules").exists()


def test_sync_no_config(tmp_path: Path) -> None:
    result = runner.invoke(app, ["sync", "--dir", str(tmp_path)])
    assert result.exit_code == 1


def test_status(tmp_path: Path) -> None:
    result = runner.invoke(app, ["status", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Claude" in result.output or "claude" in result.output.lower()


def test_add_rule(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["add", "New important rule", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Added" in result.output


def test_remove_rule(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["remove", "Write clean code", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Removed" in result.output


def test_rules_command(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["rules", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Write clean code" in result.output


def test_diff(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    config_path = get_config_path(tmp_path)
    write_config(config_path, sample_config)
    result = runner.invoke(app, ["diff", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "new file" in result.output


def test_tools_command() -> None:
    result = runner.invoke(app, ["tools"])
    assert result.exit_code == 0
    assert "Claude" in result.output or "CLAUDE.md" in result.output
    assert "Cursor" in result.output or ".cursorrules" in result.output


def test_import_no_existing(tmp_path: Path) -> None:
    result = runner.invoke(app, ["import", "claude", "--dir", str(tmp_path)])
    assert result.exit_code == 1
