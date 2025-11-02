"""Represents a Correlation Key."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class CorrelationKey(BaseElement):
    """A CorrelationKey is a composite key of CorrelationProperties that define extraction Expressions for Messages."""

    correlation_property_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "correlationPropertyRef",
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
        name = "correlationKey"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CorrelationKey]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "correlation_property_ref": [elem.text for elem in obj.findall("./bpmn:correlationPropertyRef")],
            }
        )

        return cls(**attribs)
