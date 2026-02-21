"""Adapter for Cline (.clinerules)."""

from __future__ import annotations

from typing import Any

from dotai.adapters.base import BaseAdapter


class ClineAdapter(BaseAdapter):
    name = "cline"
    file_name = ".clinerules"
    description = "Cline"

    def generate(self, config: dict[str, Any]) -> str:
        sections = []

        project = config.get("project", {})
        if project.get("name"):
            sections.append(f"# {project['name']}")
            sections.append("")
        if project.get("description"):
            sections.append(project["description"])
            sections.append("")

        details = []
        if project.get("language"):
            details.append(f"Language: {project['language']}")
        if project.get("framework"):
            details.append(f"Framework: {project['framework']}")
        if details:
            sections.append(" | ".join(details))
            sections.append("")

        rules = config.get("rules", [])
        if rules:
            sections.append("## Rules")
            sections.append("")
            for rule in rules:
                sections.append(f"- {rule}")
            sections.append("")

        style = config.get("style", {})
        testing = config.get("testing", {})
        style_lines = []
        if style.get("formatting"):
            style_lines.append(f"- Formatter: {style['formatting']}")
        if style.get("linting"):
            style_lines.append(f"- Linter: {style['linting']}")
        if style.get("line_length"):
            style_lines.append(f"- Line length: {style['line_length']}")
        if testing.get("framework"):
            style_lines.append(f"- Tests: {testing['framework']}")
        if testing.get("coverage_target"):
            style_lines.append(f"- Coverage: {testing['coverage_target']}%")
        if style_lines:
            sections.append("## Style")
            sections.append("")
            sections.extend(style_lines)
            sections.append("")

        return "\n".join(sections).strip() + "\n"
