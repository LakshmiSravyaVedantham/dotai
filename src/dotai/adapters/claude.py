"""Adapter for Claude Code (CLAUDE.md)."""

from __future__ import annotations

from typing import Any

from dotai.adapters.base import BaseAdapter


class ClaudeAdapter(BaseAdapter):
    name = "claude"
    file_name = "CLAUDE.md"
    description = "Claude Code"

    def generate(self, config: dict[str, Any]) -> str:
        sections = []

        # Header
        project = config.get("project", {})
        title = project.get("name", "Project")
        sections.append(f"# {title}\n")
        if project.get("description"):
            sections.append(project["description"] + "\n")

        # Project info
        details = []
        if project.get("language"):
            details.append(f"- **Language**: {project['language']}")
        if project.get("framework"):
            details.append(f"- **Framework**: {project['framework']}")
        if details:
            sections.append("\n".join(details) + "\n")

        # Rules
        rules = config.get("rules", [])
        if rules:
            sections.append("## Rules\n")
            for rule in rules:
                sections.append(f"- {rule}")
            sections.append("")

        # Style
        style = config.get("style", {})
        testing = config.get("testing", {})
        style_lines = []
        if style.get("formatting"):
            style_lines.append(f"- **Formatter**: {style['formatting']}")
        if style.get("linting"):
            style_lines.append(f"- **Linter**: {style['linting']}")
        if style.get("line_length"):
            style_lines.append(f"- **Line length**: {style['line_length']}")
        if testing.get("framework"):
            style_lines.append(f"- **Test framework**: {testing['framework']}")
        if testing.get("coverage_target"):
            style_lines.append(f"- **Coverage target**: {testing['coverage_target']}%")
        if style_lines:
            sections.append("## Style & Testing\n")
            sections.extend(style_lines)
            sections.append("")

        # Context
        context = config.get("context", {})
        if context.get("include") or context.get("exclude"):
            sections.append("## Context\n")
            if context.get("include"):
                sections.append(
                    "**Include**: " + ", ".join(f"`{p}`" for p in context["include"])
                )
            if context.get("exclude"):
                sections.append(
                    "**Exclude**: " + ", ".join(f"`{p}`" for p in context["exclude"])
                )
            sections.append("")

        return "\n".join(sections).strip() + "\n"
