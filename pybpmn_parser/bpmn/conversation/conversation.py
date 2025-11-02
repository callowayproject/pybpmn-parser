"""Represents a Conversation."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Conversation(ConversationNode):
    """A Conversation is a logical grouping of Message exchanges (Message Flows) that can share a Correlation."""

    class Meta:
        name = "conversation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
