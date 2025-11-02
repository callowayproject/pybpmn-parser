"""Represents a BPMN 2.0 message flow association."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[MessageFlowAssociation]:
        """Parse an XML object into a MessageFlowAssociation object."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "inner_message_flow_ref": obj.get("innerMessageFlowRef"),
                "outer_message_flow_ref": obj.get("outerMessageFlowRef"),
            }
        )
        return cls(**attribs)
