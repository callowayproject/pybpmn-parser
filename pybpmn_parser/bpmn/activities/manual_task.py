"""Represents a Manual Task."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ManualTask(Task):
    """A Manual Task is a Task that requires human interaction."""

    class Meta:
        name = "manualTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
