"""Adapter for GitHub Copilot (.github/copilot-instructions.md)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotai.adapters.base import BaseAdapter


class CopilotAdapter(BaseAdapter):
    name = "copilot"
    file_name = ".github/copilot-instructions.md"
    description = "GitHub Copilot"

    def get_output_path(self, project_dir: Path) -> Path:
        return project_dir / ".github" / "copilot-instructions.md"

    def generate(self, config: dict[str, Any]) -> str:
        sections = []

        # Project
        project = config.get("project", {})
        if project.get("name"):
            sections.append(f"# {project['name']}")
            sections.append("")
        if project.get("description"):
            sections.append(project["description"])
            sections.append("")

        # Tech stack
        details = []
        if project.get("language"):
            details.append(f"- Language: {project['language']}")
        if project.get("framework"):
            details.append(f"- Framework: {project['framework']}")
        style = config.get("style", {})
        if style.get("formatting"):
            details.append(f"- Formatter: {style['formatting']}")
        if style.get("linting"):
            details.append(f"- Linter: {style['linting']}")
        testing = config.get("testing", {})
        if testing.get("framework"):
            details.append(f"- Testing: {testing['framework']}")
        if details:
            sections.append("## Tech Stack")
            sections.append("")
            sections.extend(details)
            sections.append("")

        # Instructions (from rules)
        rules = config.get("rules", [])
        if rules:
            sections.append("## Instructions")
            sections.append("")
            for rule in rules:
                sections.append(f"- {rule}")
            sections.append("")

        # Style
        style_lines = []
        if style.get("line_length"):
            style_lines.append(f"- Keep lines under {style['line_length']} characters")
        if testing.get("coverage_target"):
            style_lines.append(f"- Aim for {testing['coverage_target']}% test coverage")
        if style_lines:
            sections.append("## Code Style")
            sections.append("")
            sections.extend(style_lines)
            sections.append("")

        return "\n".join(sections).strip() + "\n"
