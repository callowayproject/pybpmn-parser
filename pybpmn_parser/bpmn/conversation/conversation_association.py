"""Represents a Conversation Association."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


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
