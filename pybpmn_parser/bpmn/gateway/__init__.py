"""Represents a BPMN 2.0 gateway."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_node import FlowNode
from pybpmn_parser.bpmn.types import GatewayDirection
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class Gateway(FlowNode):  # Is Abstract
    """Gateways are used to control how the Process flows through SequenceFlows as they converge and diverge."""

    class Meta:
        name = "gateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    gateway_direction: GatewayDirection = field(
        default=GatewayDirection.UNSPECIFIED,
        metadata={
            "name": "gatewayDirection",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Gateway]:
        """Parse the given XML element."""
        if obj is None:
            return None

        baseclass = FlowNode.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "gateway_direction": obj.get("gatewayDirection"),
            }
        )
        return cls(**attribs)
