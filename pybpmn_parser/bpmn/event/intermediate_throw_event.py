"""Represents an intermediate throw event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class IntermediateThrowEvent(ThrowEvent):
    """The IntermediateThrowEvent triggers an event somewhere between the start and end of a Process."""

    class Meta:
        name = "intermediateThrowEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
