"""Representation of a BPMN CallConversation element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CallConversation]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation

        if obj is None:
            return None

        baseclass = ConversationNode.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "called_collaboration_ref": obj.get("calledCollaborationRef"),
                "participant_associations": [
                    ParticipantAssociation.parse(elem)
                    for elem in obj.findall("./bpmn:participationAssociation", NAMESPACES)
                ],
            }
        )
        return cls(**attribs)
