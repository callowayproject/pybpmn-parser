"""Represents a signal event definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class SignalEventDefinition(EventDefinition):
    """The definition of a Signal event."""

    class Meta:
        name = "signalEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    signal_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "signalRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
