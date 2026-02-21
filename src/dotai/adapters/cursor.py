"""Adapter for Cursor (.cursorrules)."""

from __future__ import annotations

from typing import Any

from dotai.adapters.base import BaseAdapter


class CursorAdapter(BaseAdapter):
    name = "cursor"
    file_name = ".cursorrules"
    description = "Cursor"

    def generate(self, config: dict[str, Any]) -> str:
        sections = []

        # Project context
        project = config.get("project", {})
        if project.get("name"):
            sections.append(f"You are working on {project['name']}.")
        if project.get("description"):
            sections.append(project["description"])
        if project.get("language"):
            lang = project["language"]
            fw = project.get("framework", "")
            if fw:
                sections.append(f"This is a {lang} project using {fw}.")
            else:
                sections.append(f"This is a {lang} project.")

        sections.append("")

        # Rules
        rules = config.get("rules", [])
        if rules:
            sections.append("Rules:")
            for rule in rules:
                sections.append(f"- {rule}")
            sections.append("")

        # Style
        style = config.get("style", {})
        testing = config.get("testing", {})
        style_lines = []
        if style.get("formatting"):
            style_lines.append(f"- Use {style['formatting']} for code formatting")
        if style.get("linting"):
            style_lines.append(f"- Use {style['linting']} for linting")
        if style.get("line_length"):
            style_lines.append(f"- Maximum line length: {style['line_length']}")
        if testing.get("framework"):
            style_lines.append(f"- Use {testing['framework']} for testing")
        if testing.get("coverage_target"):
            style_lines.append(f"- Target {testing['coverage_target']}% test coverage")
        if style_lines:
            sections.append("Code style:")
            sections.extend(style_lines)
            sections.append("")

        # Context
        context = config.get("context", {})
        if context.get("exclude"):
            sections.append(
                "Do not modify or reference files in: " + ", ".join(context["exclude"])
            )
            sections.append("")

        return "\n".join(sections).strip() + "\n"
