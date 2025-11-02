"""Represents a Message Event Definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class MessageEventDefinition(EventDefinition):
    """Represents a Message Event Definition."""

    class Meta:
        name = "messageEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    operation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[MessageEventDefinition]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        operation_ref = obj.find("./bpmn:operationRef", NAMESPACES)
        attribs.update(
            {
                "operation_ref": operation_ref.text if operation_ref is not None else None,
                "message_ref": obj.get("messageRef"),
            }
        )

        return cls(**attribs)
