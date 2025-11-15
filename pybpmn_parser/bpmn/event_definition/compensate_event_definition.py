"""Represents a Compensate Event Definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class CompensateEventDefinition(EventDefinition):
    """The definition of a CompensateEvent."""

    class Meta:
        name = "compensateEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    wait_for_completion: bool = field(
        default=True,
        metadata={
            "name": "waitForCompletion",
            "type": "Attribute",
        },
    )
    activity_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "activityRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
