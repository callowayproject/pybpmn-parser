"""Represents a Resource."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
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
