"""Represents a Message Event Definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class MessageEventDefinition(EventDefinition):
    """Represents a Message Event Definition."""

    class Meta:
        name = "messageEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    operation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
