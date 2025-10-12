"""Represents a Manual Task."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.activities.task import Task


@dataclass(kw_only=True)
class ManualTask(Task):
    """A Manual Task is a Task that requires human interaction."""

    pass
