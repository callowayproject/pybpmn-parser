"""Represents a Message."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Message]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "item_ref": obj.get("itemRef"),
            }
        )
        return cls(**attribs)
