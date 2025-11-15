"""Represents a boundary event."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.event.catch_event import CatchEvent
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class BoundaryEvent(CatchEvent):
    """The Boundary Event is a special kind of Catch Event that is attached to a specific Activity."""

    cancel_activity: bool = field(
        default=True,
        metadata={
            "name": "cancelActivity",
            "type": "Attribute",
        },
    )
    attached_to_ref: str = field(
        metadata={
            "name": "attachedToRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "boundaryEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
