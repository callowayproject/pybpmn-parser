"""Represents a Terminate Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class TerminateEventDefinition(EventDefinition):
    """The definition of a terminate event."""

    class Meta:
        name = "terminateEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
