"""Tests for dotai adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotai.adapters.aider import AiderAdapter
from dotai.adapters.claude import ClaudeAdapter
from dotai.adapters.cline import ClineAdapter
from dotai.adapters.copilot import CopilotAdapter
from dotai.adapters.cursor import CursorAdapter
from dotai.adapters.windsurf import WindsurfAdapter


def test_claude_adapter(sample_config: dict[str, Any]) -> None:
    adapter = ClaudeAdapter()
    content = adapter.generate(sample_config)
    assert "myapp" in content
    assert "Write clean code" in content
    assert "python" in content
    assert "fastapi" in content
    assert "black" in content
    assert "ruff" in content
    assert "pytest" in content


def test_claude_adapter_write(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = ClaudeAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.exists()
    assert path.name == "CLAUDE.md"
    content = path.read_text(encoding="utf-8")
    assert "myapp" in content


def test_cursor_adapter(sample_config: dict[str, Any]) -> None:
    adapter = CursorAdapter()
    content = adapter.generate(sample_config)
    assert "myapp" in content
    assert "python" in content
    assert "Write clean code" in content
    assert "black" in content


def test_cursor_adapter_file(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = CursorAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.name == ".cursorrules"


def test_copilot_adapter(sample_config: dict[str, Any]) -> None:
    adapter = CopilotAdapter()
    content = adapter.generate(sample_config)
    assert "myapp" in content
    assert "python" in content
    assert "Write clean code" in content


def test_copilot_adapter_path(tmp_path: Path) -> None:
    adapter = CopilotAdapter()
    path = adapter.get_output_path(tmp_path)
    assert path == tmp_path / ".github" / "copilot-instructions.md"


def test_copilot_adapter_write(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = CopilotAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.exists()
    assert path.parent.name == ".github"


def test_windsurf_adapter(sample_config: dict[str, Any]) -> None:
    adapter = WindsurfAdapter()
    content = adapter.generate(sample_config)
    assert "myapp" in content
    assert "python" in content
    assert "Write clean code" in content


def test_windsurf_adapter_file(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = WindsurfAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.name == ".windsurfrules"


def test_cline_adapter(sample_config: dict[str, Any]) -> None:
    adapter = ClineAdapter()
    content = adapter.generate(sample_config)
    assert "myapp" in content
    assert "Write clean code" in content
    assert "python" in content


def test_cline_adapter_file(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = ClineAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.name == ".clinerules"


def test_aider_adapter(sample_config: dict[str, Any]) -> None:
    adapter = AiderAdapter()
    content = adapter.generate(sample_config)
    assert "python" in content.lower() or "Python" in content
    assert "ruff" in content
    assert "pytest" in content


def test_aider_adapter_file(tmp_path: Path, sample_config: dict[str, Any]) -> None:
    adapter = AiderAdapter()
    path = adapter.write(tmp_path, sample_config)
    assert path.name == ".aider.conf.yml"


def test_adapter_exists(tmp_path: Path) -> None:
    adapter = ClaudeAdapter()
    assert not adapter.exists(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("test", encoding="utf-8")
    assert adapter.exists(tmp_path)


def test_adapter_read_existing(tmp_path: Path) -> None:
    adapter = ClaudeAdapter()
    assert adapter.read_existing(tmp_path) is None
    (tmp_path / "CLAUDE.md").write_text("hello", encoding="utf-8")
    assert adapter.read_existing(tmp_path) == "hello"


def test_all_adapters_have_names() -> None:
    from dotai.adapters import ALL_ADAPTERS

    for cls in ALL_ADAPTERS:
        adapter = cls()
        assert adapter.name, f"{cls.__name__} missing name"
        assert adapter.file_name, f"{cls.__name__} missing file_name"
        assert adapter.description, f"{cls.__name__} missing description"


def test_minimal_config() -> None:
    """All adapters should handle a minimal config without errors."""
    from dotai.adapters import ALL_ADAPTERS

    minimal: dict[str, Any] = {"version": 1}
    for cls in ALL_ADAPTERS:
        adapter = cls()
        content = adapter.generate(minimal)
        assert isinstance(content, str)
