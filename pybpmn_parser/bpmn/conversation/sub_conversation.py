"""Represents a SubConversation element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
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
            "name": "conversation",
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
