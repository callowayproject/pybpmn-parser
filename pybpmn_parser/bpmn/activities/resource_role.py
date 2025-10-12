"""Represents a Resource Role."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.activities.resource_assignment_expression import ResourceAssignmentExpression
    from pybpmn_parser.bpmn.common.resource_parameter_binding import ResourceParameterBinding


@dataclass(kw_only=True)
class ResourceRole(BaseElement):
    """Defines how Resources can be defined for an Activity."""

    resource_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "resourceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    resource_parameter_binding: list[ResourceParameterBinding] = field(
        default_factory=list,
        metadata={
            "name": "resourceParameterBinding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    resource_assignment_expression: Optional[ResourceAssignmentExpression] = field(
        default=None,
        metadata={
            "name": "resourceAssignmentExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ResourceRole]:
        """Parse an XML element into a ResourceRole object."""
        from pybpmn_parser.bpmn.activities.resource_assignment_expression import ResourceAssignmentExpression
        from pybpmn_parser.bpmn.common.resource_parameter_binding import ResourceParameterBinding

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        resource_ref = obj.find("./bpmn:resourceRef", NAMESPACES)
        resource_parameter_binding = obj.findall("./bpmn:resourceParameterBinding", NAMESPACES)
        resource_assignment_expression = obj.find("./bpmn:resourceAssignmentExpression", NAMESPACES)
        attributes.update(
            {
                "resource_ref": resource_ref.text if resource_ref is not None else None,
                "name": obj.get("name"),
                "resource_parameter_binding": [
                    ResourceParameterBinding.parse(elem) for elem in resource_parameter_binding
                ],
                "resource_assignment_expression": ResourceAssignmentExpression.parse(resource_assignment_expression),
            }
        )
        return cls(**attributes)
