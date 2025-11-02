"""Represents a link event definition."""

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
class LinkEventDefinition(EventDefinition):
    """The LinkEventDefinition element is used for specifying a link event definition."""

    class Meta:
        name = "linkEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    sources: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    target: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[LinkEventDefinition]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        target = obj.find("./bpmn:target", NAMESPACES)
        attribs.update(
            {
                "name": obj.get("name", ""),
                "target": target.text if target is not None else None,
                "sources": [elem.text for elem in obj.findall("./bpmn:source", NAMESPACES)],
            }
        )

        return cls(**attribs)
