"""Represents a Relationship."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.types import RelationshipDirection


@dataclass(kw_only=True)
class Relationship(BaseElement):
    """A Relationship defines a relationship between two Elements."""

    source: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "is_reference": True,
        },
    )
    """This association defines artifacts that are augmented by the relationship."""

    target: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "is_reference": True,
        },
    )
    """This association defines artifacts used to extend the semantics of the source element(s)."""

    type_value: str = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    """The descriptive name of the element."""

    direction: Optional[RelationshipDirection] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute specifies the direction of the relationship."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Relationship]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "type_value": obj.get("type"),
                "direction": obj.get("direction"),
                "source": [elem.text for elem in obj.findall("./bpmn:source", NAMESPACES)],
                "target": [elem.text for elem in obj.findall("./bpmn:target", NAMESPACES)],
            }
        )
        return cls(**attribs)
