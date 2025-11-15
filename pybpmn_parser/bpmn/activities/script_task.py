"""Represents a Script Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ScriptTask(Task):
    """A Script Task is executed by a business process engine."""

    script: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    script_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "scriptFormat",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "scriptTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
