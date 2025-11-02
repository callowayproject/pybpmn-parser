"""Represents an implicit throw event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ImplicitThrowEvent(ThrowEvent):
    """The ImplicitThrowEvent is a non-graphical Event used for complex Multi-Instance Activities."""

    class Meta:
        name = "implicitThrowEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
