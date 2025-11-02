"""Represents a BPMN 2.0 conversation node."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey


@register_element
@dataclass(kw_only=True)
class ConversationNode(BaseElement):
    """ConversationNode is the abstract super class for all Conversation bpmn of a Collaboration diagram."""

    participant_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "participantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    message_flow_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "messageFlowRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    correlation_keys: list[CorrelationKey] = field(
        default_factory=list,
        metadata={
            "name": "correlationKey",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "conversationNode"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ConversationNode]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "correlation_keys": [
                    CorrelationKey.parse(elem) for elem in obj.findall("./bpmn:correlationKey", NAMESPACES)
                ],
                "message_flow_refs": [elem.text for elem in obj.findall("./bpmn:messageFlowRef", NAMESPACES)],
                "name": obj.get("name"),
                "participant_refs": [elem.text for elem in obj.findall("./bpmn:participantRef", NAMESPACES)],
            }
        )
        return cls(**attribs)
