"""Represents an intermediate catch event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.catch_event import CatchEvent
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class IntermediateCatchEvent(CatchEvent):
    """The IntermediateCatchEvent catches an event that happens somewhere between the start and end of a Process."""

    class Meta:
        name = "intermediateCatchEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
