"""Represents a BPMN 2.0 message flow association."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class MessageFlowAssociation(BaseElement):
    """A MessageFlowAssociation links an (outer) diagram Message Flows to an (inner) diagram Message Flows."""

    inner_message_flow_ref: str = field(
        metadata={
            "name": "innerMessageFlowRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    outer_message_flow_ref: str = field(
        metadata={
            "name": "outerMessageFlowRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "messageFlowAssociation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
