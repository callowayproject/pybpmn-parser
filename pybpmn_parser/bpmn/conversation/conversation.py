"""Represents a Conversation."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode


@dataclass(kw_only=True)
class Conversation(ConversationNode):
    """A Conversation is a logical grouping of Message exchanges (Message Flows) that can share a Correlation."""

    pass
