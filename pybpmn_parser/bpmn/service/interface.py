"""Represents an Interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
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
