"""Represents an end event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class EndEvent(ThrowEvent):
    """The End Event indicates where a Process will end."""

    class Meta:
        name = "endEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
