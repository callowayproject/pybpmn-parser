"""Represents a Conversation Association."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class ConversationAssociation(BaseElement):
    """A ConversationAssociation allows a reusable Conversation within Collaborations/Choreographies."""

    inner_conversation_node_ref: str = field(
        metadata={
            "name": "innerConversationNodeRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    outer_conversation_node_ref: str = field(
        metadata={
            "name": "outerConversationNodeRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "conversationAssociation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ConversationAssociation]:
        """Parse an XML object into a ConversationAssociation object."""
        if obj is None:
            return None
        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "inner_conversation_node_ref": obj.get("innerConversationNodeRef"),
                "outer_conversation_node_ref": obj.get("outerConversationNodeRef"),
            }
        )
        return cls(**attribs)
