"""Represents an escalation event definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class EscalationEventDefinition(EventDefinition):
    """The definition of an escalation event."""

    class Meta:
        name = "escalationEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    escalation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "escalationRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[EscalationEventDefinition]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "escalation_ref": obj.get("escalationRef"),
            }
        )

        return cls(**attribs)
