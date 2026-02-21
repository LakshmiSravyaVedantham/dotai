"""Core config: read/write the central .ai/config.yml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = ".ai"
CONFIG_FILE = "config.yml"
DEFAULT_VERSION = 1


def get_config_path(project_dir: Path | None = None) -> Path:
    """Get the path to the central config file."""
    base = project_dir or Path.cwd()
    return base / CONFIG_DIR / CONFIG_FILE


def read_config(config_path: Path) -> dict[str, Any]:
    """Read the central .ai/config.yml."""
    if not config_path.exists():
        return {}
    text = config_path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def write_config(config_path: Path, config: dict[str, Any]) -> None:
    """Write the central .ai/config.yml."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.dump(config, default_flow_style=False, sort_keys=False, width=120),
        encoding="utf-8",
    )


def create_default_config() -> dict[str, Any]:
    """Create a default config template."""
    return {
        "version": DEFAULT_VERSION,
        "project": {
            "name": "",
            "description": "",
            "language": "",
            "framework": "",
        },
        "rules": [
            "Write clean, readable code with meaningful names",
            "Add type hints to all function signatures",
            "Follow the existing code style and patterns",
            "Write tests for new functionality",
        ],
        "context": {
            "include": ["src/", "tests/", "README.md"],
            "exclude": [
                "node_modules/",
                ".env",
                "__pycache__/",
                ".git/",
                "dist/",
                "build/",
            ],
        },
        "style": {
            "formatting": "",
            "linting": "",
            "line_length": 88,
        },
        "testing": {
            "framework": "",
            "coverage_target": 80,
        },
    }


def add_rule(config: dict[str, Any], rule: str) -> dict[str, Any]:
    """Add a rule to the config."""
    if "rules" not in config:
        config["rules"] = []
    if rule not in config["rules"]:
        config["rules"].append(rule)
    return config


def remove_rule(config: dict[str, Any], rule: str) -> bool:
    """Remove a rule. Returns True if removed."""
    rules = config.get("rules", [])
    if rule in rules:
        rules.remove(rule)
        return True
    return False


def detect_project_info(project_dir: Path | None = None) -> dict[str, str]:
    """Auto-detect project language, framework, etc."""
    base = project_dir or Path.cwd()
    info: dict[str, str] = {}

    # Detect language
    if (base / "pyproject.toml").exists() or (base / "requirements.txt").exists():
        info["language"] = "python"
    elif (base / "package.json").exists():
        info["language"] = "javascript"
    elif (base / "go.mod").exists():
        info["language"] = "go"
    elif (base / "Cargo.toml").exists():
        info["language"] = "rust"
    elif (base / "Gemfile").exists():
        info["language"] = "ruby"

    # Detect framework
    if info.get("language") == "python":
        if (base / "manage.py").exists():
            info["framework"] = "django"
        elif _file_contains(base / "pyproject.toml", "fastapi"):
            info["framework"] = "fastapi"
        elif _file_contains(base / "pyproject.toml", "flask"):
            info["framework"] = "flask"
    elif info.get("language") == "javascript":
        if _file_contains(base / "package.json", "next"):
            info["framework"] = "nextjs"
        elif _file_contains(base / "package.json", "react"):
            info["framework"] = "react"
        elif _file_contains(base / "package.json", "vue"):
            info["framework"] = "vue"
        elif _file_contains(base / "package.json", "express"):
            info["framework"] = "express"

    # Detect formatting/linting
    if (base / "pyproject.toml").exists():
        content = (base / "pyproject.toml").read_text(encoding="utf-8")
        if "black" in content or "ruff.format" in content:
            info["formatting"] = "black" if "black" in content else "ruff"
        if "ruff" in content:
            info["linting"] = "ruff"
        elif "flake8" in content:
            info["linting"] = "flake8"

    # Detect test framework
    if (base / "pytest.ini").exists() or _file_contains(
        base / "pyproject.toml", "pytest"
    ):
        info["testing"] = "pytest"
    elif (base / "jest.config.js").exists() or (base / "jest.config.ts").exists():
        info["testing"] = "jest"

    # Detect project name
    if (base / "pyproject.toml").exists():
        try:
            content = (base / "pyproject.toml").read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.strip().startswith("name"):
                    name = line.split("=", 1)[1].strip().strip('"').strip("'")
                    info["name"] = name
                    break
        except OSError:
            pass
    elif (base / "package.json").exists():
        try:
            import json

            pkg = json.loads((base / "package.json").read_text(encoding="utf-8"))
            info["name"] = pkg.get("name", "")
        except (OSError, ValueError):
            pass

    if not info.get("name"):
        info["name"] = base.name

    return info


def _file_contains(path: Path, text: str) -> bool:
    """Check if a file exists and contains given text."""
    try:
        return text in path.read_text(encoding="utf-8")
    except OSError:
        return False
