"""Represents a Resource Role."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.resource_assignment_expression import ResourceAssignmentExpression
    from pybpmn_parser.bpmn.common.resource_parameter_binding import ResourceParameterBinding


@register_element
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

    class Meta:
        name = "resourceRole"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
