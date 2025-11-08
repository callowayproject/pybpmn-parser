"""Represents an Interface."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.service.operation import Operation


@register_element
@dataclass(kw_only=True)
class Interface(RootElement):
    """An Interface defines a set of operations that Services implement."""

    class Meta:
        name = "interface"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    operations: list[Operation] = field(
        default_factory=list,
        metadata={
            "name": "operation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
        },
    )
    """This attribute specifies operations that are defined as part of the Interface.

    An Interface has at least one Operation."""

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """The descriptive name of the element."""

    implementation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "implementationRef",
            "type": "Attribute",
        },
    )
    """A reference to a concrete artifact in the underlying implementation technology that represents the interface."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Interface]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.service.operation import Operation

        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "implementation_ref": obj.get("implementationRef"),
                "operations": [Operation.parse(elem) for elem in obj.findall("./bpmn:operation", NAMESPACES)],
            }
        )
        return cls(**attribs)
