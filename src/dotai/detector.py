"""Detect which AI coding tools are in use in a project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotai.adapters import ALL_ADAPTERS
from dotai.adapters.base import BaseAdapter


@dataclass
class ToolStatus:
    """Status of an AI tool in the project."""

    name: str
    description: str
    file_name: str
    exists: bool
    path: Path


def detect_tools(project_dir: Path | None = None) -> list[ToolStatus]:
    """Detect which AI tool configs exist in the project."""
    base = project_dir or Path.cwd()
    results = []
    for adapter_cls in ALL_ADAPTERS:
        adapter: BaseAdapter = adapter_cls()
        path = adapter.get_output_path(base)
        results.append(
            ToolStatus(
                name=adapter.name,
                description=adapter.description,
                file_name=adapter.file_name,
                exists=path.exists(),
                path=path,
            )
        )
    return results


def get_active_tools(project_dir: Path | None = None) -> list[ToolStatus]:
    """Get only the tools that have config files present."""
    return [t for t in detect_tools(project_dir) if t.exists]


def get_adapter_by_name(name: str) -> BaseAdapter | None:
    """Get an adapter instance by tool name."""
    for adapter_cls in ALL_ADAPTERS:
        adapter: BaseAdapter = adapter_cls()
        if adapter.name == name:
            return adapter
    return None
