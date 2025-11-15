"""Represents a Group."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.common.artifact import Artifact
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Group(Artifact):
    """Groups are often used to highlight certain subclauses of a Diagram without adding additional constraints."""

    category_value_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "categoryValueRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "group"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
