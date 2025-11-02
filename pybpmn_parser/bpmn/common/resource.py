"""Represents a Resource."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.resource_parameter import ResourceParameter


@register_element
@dataclass(kw_only=True)
class Resource(RootElement):
    """The Resource class is used to specify resources that can be referenced by Activities."""

    resource_parameters: list[ResourceParameter] = field(
        default_factory=list,
        metadata={
            "name": "resourceParameter",
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

    class Meta:
        name = "resource"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Resource]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.common.resource_parameter import ResourceParameter

        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "resource_parameters": [
                    ResourceParameter.parse(elem) for elem in obj.findall("./bpmn:resourceParameter", NAMESPACES)
                ],
            }
        )
        return cls(**attribs)
