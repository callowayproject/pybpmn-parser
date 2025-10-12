"""Representation of a BPMN CallableElement."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.io_binding import IoBinding
    from pybpmn_parser.bpmn.data.io_specification import IoSpecification


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CallableElement]:
        """Parse an XML element into a CallableElement object."""
        from pybpmn_parser.bpmn.data.io_binding import IoBinding
        from pybpmn_parser.bpmn.data.io_specification import IoSpecification

        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        attribs.update(
            {
                "name": obj.get("name"),
                "io_bindings": [IoBinding.parse(elem) for elem in obj.findall("./bpmn:ioBinding", NAMESPACES)],
                "io_specification": IoSpecification.parse(obj.find("./bpmn:ioSpecification", NAMESPACES)),
                "supported_interface_refs": [
                    elem.text for elem in obj.findall("./bpmn:supportedInterfaceRef", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
