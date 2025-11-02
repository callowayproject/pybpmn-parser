"""Represents a ConditionalEventDefinition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class ConditionalEventDefinition(EventDefinition):
    """Definition of a conditional event."""

    class Meta:
        name = "conditionalEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    condition: Expression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ConditionalEventDefinition]:
        """Parse an XML element into a ConditionalEventDefinition object."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "condition": Expression.parse(obj.find("./bpmn:condition", NAMESPACES)),
            }
        )

        return cls(**attribs)
