"""Represents a Cancel Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class CancelEventDefinition(EventDefinition):
    """The definition of a cancel event."""

    class Meta:
        name = "cancelEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
