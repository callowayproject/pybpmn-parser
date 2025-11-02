"""Representation of an Assignment."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class Assignment(BaseElement):
    """Assignment is used to specify a simple mapping of data bpmn using a specified Expression language."""

    from_value: Expression = field(
        metadata={
            "name": "from",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    to: Expression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )

    class Meta:
        name = "assignment"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Assignment]:
        """Parse an XML object into an Assignment object."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "from_value": Expression.parse(obj.find("./bpmn:from", NAMESPACES)),
                "to": Expression.parse(obj.find("./bpmn:to", NAMESPACES)),
            }
        )

        return cls(**attribs)
