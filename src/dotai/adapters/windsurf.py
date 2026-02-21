"""Adapter for Windsurf (.windsurfrules)."""

from __future__ import annotations

from typing import Any

from dotai.adapters.base import BaseAdapter


class WindsurfAdapter(BaseAdapter):
    name = "windsurf"
    file_name = ".windsurfrules"
    description = "Windsurf"

    def generate(self, config: dict[str, Any]) -> str:
        sections = []

        project = config.get("project", {})
        if project.get("name"):
            sections.append(f"Project: {project['name']}")
        if project.get("description"):
            sections.append(project["description"])
        if project.get("language"):
            lang = project["language"]
            fw = project.get("framework", "")
            if fw:
                sections.append(f"Tech: {lang} + {fw}")
            else:
                sections.append(f"Tech: {lang}")

        sections.append("")

        rules = config.get("rules", [])
        if rules:
            sections.append("Rules:")
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
            style_lines.append(f"- Max line length: {style['line_length']}")
        if testing.get("framework"):
            style_lines.append(f"- Test framework: {testing['framework']}")
        if style_lines:
            sections.append("Style:")
            sections.extend(style_lines)
            sections.append("")

        return "\n".join(sections).strip() + "\n"
