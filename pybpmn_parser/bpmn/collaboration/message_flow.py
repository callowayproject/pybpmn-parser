"""Represents a Message Flow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class MessageFlow(BaseElement):
    """A Message Flow is used to show the flow of Messages between two Participants."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    source_ref: str = field(
        metadata={
            "name": "sourceRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "messageFlow"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
