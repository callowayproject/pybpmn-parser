"""Represents a Message."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Message(RootElement):
    """A Message represents the content of a communication between two Participants."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    item_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "itemRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "message"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
