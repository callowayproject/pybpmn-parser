"""Represents a Conversation Link."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ConversationLink(BaseElement):
    """Conversation Links are used to connect ConversationNodes to and from Participants."""

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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ConversationLink]:
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
            }
        )
        return cls(**attributes)
