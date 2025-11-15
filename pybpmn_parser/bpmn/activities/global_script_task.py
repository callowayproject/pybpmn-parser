"""Represents a Global Script Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class GlobalScriptTask(GlobalTask):
    """A type of Global Task that represents a Script Task."""

    script: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    script_language: Optional[str] = field(
        default=None,
        metadata={
            "name": "scriptLanguage",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "globalScriptTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
