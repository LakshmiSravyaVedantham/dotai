"""Shared test fixtures for dotai tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """A sample config for testing."""
    return {
        "version": 1,
        "project": {
            "name": "myapp",
            "description": "A sample application",
            "language": "python",
            "framework": "fastapi",
        },
        "rules": [
            "Write clean code",
            "Add type hints",
            "Write tests for new code",
        ],
        "context": {
            "include": ["src/", "tests/"],
            "exclude": ["node_modules/", ".env", "__pycache__/"],
        },
        "style": {
            "formatting": "black",
            "linting": "ruff",
            "line_length": 88,
        },
        "testing": {
            "framework": "pytest",
            "coverage_target": 90,
        },
    }


@pytest.fixture
def python_project(tmp_path: Path) -> Path:
    """Create a temporary Python project with common files."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "testproj"\n\n[tool.ruff]\nselect = ["E"]\n\n'
        "[tool.pytest.ini_options]\ntestpaths = ['tests']\n",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    return tmp_path


@pytest.fixture
def js_project(tmp_path: Path) -> Path:
    """Create a temporary JavaScript project."""
    (tmp_path / "package.json").write_text(
        '{"name": "testapp", "dependencies": {"react": "^18.0.0"}}',
        encoding="utf-8",
    )
    return tmp_path
