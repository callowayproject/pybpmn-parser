"""Represents an escalation event definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class EscalationEventDefinition(EventDefinition):
    """The definition of an escalation event."""

    class Meta:
        name = "escalationEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    escalation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "escalationRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
