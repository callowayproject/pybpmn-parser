"""Representation of a BPMN CallConversation element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation


@register_element
@dataclass(kw_only=True)
class CallConversation(ConversationNode):
    """A Call Conversation identifies a place in the Conversation (Collaboration) where a global Conversation."""

    participant_associations: list[ParticipantAssociation] = field(
        default_factory=list,
        metadata={
            "name": "participantAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    called_collaboration_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "calledCollaborationRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "callConversation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
