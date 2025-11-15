"""Represents an Escalation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Escalation(RootElement):
    """An Escalation identifies a business situation that a Process might need to react to."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    escalation_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "escalationCode",
            "type": "Attribute",
        },
    )
    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "escalation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
