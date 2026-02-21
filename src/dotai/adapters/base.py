"""Base adapter class for AI tool config generation."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any


class BaseAdapter(abc.ABC):
    """Base class for all AI tool adapters."""

    name: str = ""
    file_name: str = ""
    description: str = ""

    @abc.abstractmethod
    def generate(self, config: dict[str, Any]) -> str:
        """Generate the tool-specific config content from central config."""

    def get_output_path(self, project_dir: Path) -> Path:
        """Get the output file path for this adapter."""
        return project_dir / self.file_name

    def write(self, project_dir: Path, config: dict[str, Any]) -> Path:
        """Generate and write the config file. Returns the path written."""
        content = self.generate(config)
        output_path = self.get_output_path(project_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path

    def exists(self, project_dir: Path) -> bool:
        """Check if this tool's config already exists."""
        return self.get_output_path(project_dir).exists()

    def read_existing(self, project_dir: Path) -> str | None:
        """Read existing config file content, if any."""
        path = self.get_output_path(project_dir)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def _build_rules_block(self, config: dict[str, Any]) -> str:
        """Build a formatted rules block from config."""
        rules = config.get("rules", [])
        if not rules:
            return ""
        lines = ["## Rules", ""]
        for rule in rules:
            lines.append(f"- {rule}")
        return "\n".join(lines)

    def _build_project_block(self, config: dict[str, Any]) -> str:
        """Build a project info block."""
        project = config.get("project", {})
        parts = []
        if project.get("name"):
            parts.append(f"# {project['name']}")
        if project.get("description"):
            parts.append(f"\n{project['description']}")
        details = []
        if project.get("language"):
            details.append(f"- **Language**: {project['language']}")
        if project.get("framework"):
            details.append(f"- **Framework**: {project['framework']}")
        if details:
            parts.append("")
            parts.extend(details)
        return "\n".join(parts)

    def _build_context_block(self, config: dict[str, Any]) -> str:
        """Build context include/exclude block."""
        context = config.get("context", {})
        parts = []
        includes = context.get("include", [])
        excludes = context.get("exclude", [])
        if includes:
            parts.append("## Context")
            parts.append("")
            parts.append("### Include")
            for inc in includes:
                parts.append(f"- `{inc}`")
        if excludes:
            parts.append("")
            parts.append("### Exclude")
            for exc in excludes:
                parts.append(f"- `{exc}`")
        return "\n".join(parts)

    def _build_style_block(self, config: dict[str, Any]) -> str:
        """Build style/formatting block."""
        style = config.get("style", {})
        testing = config.get("testing", {})
        parts = []
        if any(style.values()) or any(testing.values()):
            parts.append("## Style & Testing")
            parts.append("")
            if style.get("formatting"):
                parts.append(f"- **Formatter**: {style['formatting']}")
            if style.get("linting"):
                parts.append(f"- **Linter**: {style['linting']}")
            if style.get("line_length"):
                parts.append(f"- **Line length**: {style['line_length']}")
            if testing.get("framework"):
                parts.append(f"- **Test framework**: {testing['framework']}")
            if testing.get("coverage_target"):
                parts.append(f"- **Coverage target**: {testing['coverage_target']}%")
        return "\n".join(parts)
