"""Represents a Collaboration."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import strtobool
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.collaboration.message_flow import MessageFlow
    from pybpmn_parser.bpmn.collaboration.message_flow_association import MessageFlowAssociation
    from pybpmn_parser.bpmn.collaboration.participant import Participant
    from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation
    from pybpmn_parser.bpmn.common.artifact import Artifact
    from pybpmn_parser.bpmn.common.association import Association
    from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey
    from pybpmn_parser.bpmn.common.group import Group
    from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
    from pybpmn_parser.bpmn.conversation.call_conversation import CallConversation
    from pybpmn_parser.bpmn.conversation.conversation import Conversation
    from pybpmn_parser.bpmn.conversation.conversation_association import ConversationAssociation
    from pybpmn_parser.bpmn.conversation.conversation_link import ConversationLink
    from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
    from pybpmn_parser.bpmn.conversation.sub_conversation import SubConversation


@register_element
@dataclass(kw_only=True)
class Collaboration(RootElement):
    """A Collaboration is a group of Participants that work together to complete a Process."""

    participants: list[Participant] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    message_flows: list[MessageFlow] = field(
        default_factory=list,
        metadata={
            "name": "messageFlow",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    text_annotations: list[TextAnnotation] = field(
        default_factory=list,
        metadata={
            "name": "textAnnotation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    groups: list[Group] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    associations: list[Association] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    artifacts: list[Artifact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
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
    conversation_associations: list[ConversationAssociation] = field(
        default_factory=list,
        metadata={
            "name": "conversationAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    participant_associations: list[ParticipantAssociation] = field(
        default_factory=list,
        metadata={
            "name": "participantAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    message_flow_associations: list[MessageFlowAssociation] = field(
        default_factory=list,
        metadata={
            "name": "messageFlowAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    correlation_keys: list[CorrelationKey] = field(
        default_factory=list,
        metadata={
            "name": "correlationKey",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    choreography_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "choreographyRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    conversation_links: list[ConversationLink] = field(
        default_factory=list,
        metadata={
            "name": "conversationLink",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_closed: bool = field(
        default=False,
        metadata={
            "name": "isClosed",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "collaboration"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Collaboration]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.collaboration.message_flow import MessageFlow
        from pybpmn_parser.bpmn.collaboration.message_flow_association import MessageFlowAssociation
        from pybpmn_parser.bpmn.collaboration.participant import Participant
        from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation
        from pybpmn_parser.bpmn.common.artifact import Artifact
        from pybpmn_parser.bpmn.common.association import Association
        from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey
        from pybpmn_parser.bpmn.common.group import Group
        from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
        from pybpmn_parser.bpmn.conversation.call_conversation import CallConversation
        from pybpmn_parser.bpmn.conversation.conversation import Conversation
        from pybpmn_parser.bpmn.conversation.conversation_association import ConversationAssociation
        from pybpmn_parser.bpmn.conversation.conversation_link import ConversationLink
        from pybpmn_parser.bpmn.conversation.conversation_node import ConversationNode
        from pybpmn_parser.bpmn.conversation.sub_conversation import SubConversation

        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "artifacts": [Artifact.parse(elem) for elem in obj.findall("./bpmn:artifact", NAMESPACES)],
                "associations": [Association.parse(elem) for elem in obj.findall("./bpmn:association", NAMESPACES)],
                "call_conversations": [
                    CallConversation.parse(elem) for elem in obj.findall("./bpmn:callConversation", NAMESPACES)
                ],
                "choreography_refs": [elem.text for elem in obj.findall("./bpmn:choreographyRef", NAMESPACES)],
                "conversations": [Conversation.parse(elem) for elem in obj.findall("./bpmn:conversation", NAMESPACES)],
                "conversation_associations": [
                    ConversationAssociation.parse(elem)
                    for elem in obj.findall("./bpmn:conversationAssociation", NAMESPACES)
                ],
                "conversation_links": [
                    ConversationLink.parse(elem) for elem in obj.findall("./bpmn:conversationLink", NAMESPACES)
                ],
                "conversation_nodes": [
                    ConversationNode.parse(elem) for elem in obj.findall("./bpmn:conversationNode", NAMESPACES)
                ],
                "correlation_keys": [
                    CorrelationKey.parse(elem) for elem in obj.findall("./bpmn:correlationKey", NAMESPACES)
                ],
                "groups": [Group.parse(elem) for elem in obj.findall("./bpmn:group", NAMESPACES)],
                "is_closed": strtobool(obj.get("isClosed", "false")),
                "message_flows": [MessageFlow.parse(elem) for elem in obj.findall("./bpmn:messageFlow", NAMESPACES)],
                "message_flow_associations": [
                    MessageFlowAssociation.parse(elem)
                    for elem in obj.findall("./bpmn:messageFlowAssociation", NAMESPACES)
                ],
                "name": obj.get("name"),
                "participants": [Participant.parse(elem) for elem in obj.findall("./bpmn:participant", NAMESPACES)],
                "participant_associations": [
                    ParticipantAssociation.parse(elem)
                    for elem in obj.findall("./bpmn:participantAssociation", NAMESPACES)
                ],
                "sub_conversations": [
                    SubConversation.parse(elem) for elem in obj.findall("./bpmn:subConversation", NAMESPACES)
                ],
                "text_annotations": [
                    TextAnnotation.parse(elem) for elem in obj.findall("./bpmn:textAnnotation", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
