"""Represents a FlowNode."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class FlowNode(FlowElement):  # Is Abstract
    """The FlowNode element is used to provide a single element as the source and target Sequence Flow associations."""

    incoming: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    outgoing: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[FlowNode]:
        """Parse an XML object into a FlowElement object."""
        if obj is None:
            return None

        baseclass = FlowElement.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attributes.update(
            {
                "incoming": [elem.text for elem in obj.findall("./bpmn:incoming", NAMESPACES)],
                "outgoing": [elem.text for elem in obj.findall("./bpmn:outgoing", NAMESPACES)],
            }
        )
        return cls(**attributes)
