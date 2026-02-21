"""Adapters for syncing config to various AI coding tools."""

from dotai.adapters.aider import AiderAdapter
from dotai.adapters.claude import ClaudeAdapter
from dotai.adapters.cline import ClineAdapter
from dotai.adapters.copilot import CopilotAdapter
from dotai.adapters.cursor import CursorAdapter
from dotai.adapters.windsurf import WindsurfAdapter

ALL_ADAPTERS = [
    ClaudeAdapter,
    CursorAdapter,
    CopilotAdapter,
    WindsurfAdapter,
    ClineAdapter,
    AiderAdapter,
]

__all__ = [
    "ClaudeAdapter",
    "CursorAdapter",
    "CopilotAdapter",
    "WindsurfAdapter",
    "ClineAdapter",
    "AiderAdapter",
    "ALL_ADAPTERS",
]
