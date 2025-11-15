"""Represents an error event definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ErrorEventDefinition(EventDefinition):
    """The definition of an error event."""

    class Meta:
        name = "errorEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    error_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
