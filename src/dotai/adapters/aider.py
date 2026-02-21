"""Adapter for Aider (.aider.conf.yml)."""

from __future__ import annotations

from typing import Any

import yaml

from dotai.adapters.base import BaseAdapter


class AiderAdapter(BaseAdapter):
    name = "aider"
    file_name = ".aider.conf.yml"
    description = "Aider"

    def generate(self, config: dict[str, Any]) -> str:
        aider_config: dict[str, Any] = {}

        # Build the convention/rules string
        rules = config.get("rules", [])
        project = config.get("project", {})
        style = config.get("style", {})
        testing = config.get("testing", {})

        conventions = []
        if project.get("language"):
            conventions.append(f"Language: {project['language']}")
        if project.get("framework"):
            conventions.append(f"Framework: {project['framework']}")
        if style.get("formatting"):
            conventions.append(f"Formatter: {style['formatting']}")
        if style.get("linting"):
            conventions.append(f"Linter: {style['linting']}")
        if testing.get("framework"):
            conventions.append(f"Test framework: {testing['framework']}")
        for rule in rules:
            conventions.append(rule)

        if conventions:
            aider_config["conventions"] = "\n".join(conventions)

        # Lint command
        if style.get("linting"):
            linter = style["linting"]
            if linter == "ruff":
                aider_config["lint-cmd"] = "ruff check --fix"
            elif linter == "flake8":
                aider_config["lint-cmd"] = "flake8"
            elif linter == "eslint":
                aider_config["lint-cmd"] = "eslint --fix"

        # Test command
        if testing.get("framework"):
            tf = testing["framework"]
            if tf == "pytest":
                aider_config["test-cmd"] = "pytest"
            elif tf == "jest":
                aider_config["test-cmd"] = "npx jest"

        # Auto-commits
        aider_config["auto-commits"] = True

        return yaml.dump(
            aider_config, default_flow_style=False, sort_keys=False, width=120
        )
