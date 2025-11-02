"""Represents a SubConversation element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.conversation.call_conversation import CallConversation
    from pybpmn_parser.bpmn.conversation.conversation import Conversation


@register_element
@dataclass(kw_only=True)
class SubConversation(ConversationNode):
    """A Sub-Conversation is a ConversationNode that is a hierarchical division within the parent Collaboration."""

    sub_conversations: list[SubConversation] = field(
        default_factory=list,
        metadata={
            "name": "subConversation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    conversations: list[Conversation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    call_conversations: list[CallConversation] = field(
        default_factory=list,
        metadata={
            "name": "callConversation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    conversation_nodes: list[ConversationNode] = field(
        default_factory=list,
        metadata={
            "name": "conversationNode",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    class Meta:
        name = "subConversation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[SubConversation]:
        """Parse an XML element into a SubConversation object."""
        from pybpmn_parser.bpmn.conversation.call_conversation import CallConversation
        from pybpmn_parser.bpmn.conversation.conversation import Conversation

        if obj is None:
            return None

        baseclass = ConversationNode.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "sub_conversations": [
                    SubConversation.parse(elem) for elem in obj.findall("./bpmn:subConversation", NAMESPACES)
                ],
                "conversations": [Conversation.parse(elem) for elem in obj.findall("./bpmn:conversation", NAMESPACES)],
                "call_conversations": [
                    CallConversation.parse(elem) for elem in obj.findall("./bpmn:callConversation", NAMESPACES)
                ],
                "conversation_nodes": [
                    ConversationNode.parse(elem) for elem in obj.findall("./bpmn:conversationNode", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
