"""Represents a Message Flow."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[MessageFlow]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attributes.update(
            {
                "name": obj.get("name"),
                "source_ref": obj.get("sourceRef"),
                "target_ref": obj.get("targetRef"),
                "message_ref": obj.get("messageRef"),
            }
        )
        return cls(**attributes)
