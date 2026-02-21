"""Tests for dotai.detector module."""

from __future__ import annotations

from pathlib import Path

from dotai.detector import detect_tools, get_active_tools, get_adapter_by_name


def test_detect_tools_empty(tmp_path: Path) -> None:
    tools = detect_tools(tmp_path)
    assert len(tools) == 6
    assert all(not t.exists for t in tools)


def test_detect_tools_with_claude(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("# Test", encoding="utf-8")
    tools = detect_tools(tmp_path)
    claude = [t for t in tools if t.name == "claude"][0]
    assert claude.exists


def test_detect_tools_with_cursor(tmp_path: Path) -> None:
    (tmp_path / ".cursorrules").write_text("rules", encoding="utf-8")
    tools = detect_tools(tmp_path)
    cursor = [t for t in tools if t.name == "cursor"][0]
    assert cursor.exists


def test_get_active_tools_none(tmp_path: Path) -> None:
    active = get_active_tools(tmp_path)
    assert len(active) == 0


def test_get_active_tools_some(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("test", encoding="utf-8")
    (tmp_path / ".cursorrules").write_text("test", encoding="utf-8")
    active = get_active_tools(tmp_path)
    assert len(active) == 2


def test_get_adapter_by_name() -> None:
    adapter = get_adapter_by_name("claude")
    assert adapter is not None
    assert adapter.name == "claude"


def test_get_adapter_by_name_cursor() -> None:
    adapter = get_adapter_by_name("cursor")
    assert adapter is not None
    assert adapter.file_name == ".cursorrules"


def test_get_adapter_by_name_unknown() -> None:
    adapter = get_adapter_by_name("nonexistent")
    assert adapter is None
