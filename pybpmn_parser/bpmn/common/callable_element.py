"""Representation of a BPMN CallableElement."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.io_binding import IoBinding
    from pybpmn_parser.bpmn.data.io_specification import IoSpecification


@register_element
@dataclass(kw_only=True)
class CallableElement(RootElement):  # Is Abstract
    """A CallableElement allows it to be referenced and reused by other Processes."""

    supported_interface_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "supportedInterfaceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    io_specification: Optional[IoSpecification] = field(
        default=None,
        metadata={
            "name": "ioSpecification",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    io_bindings: list[IoBinding] = field(
        default_factory=list,
        metadata={
            "name": "ioBinding",
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
        name = "callableElement"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
