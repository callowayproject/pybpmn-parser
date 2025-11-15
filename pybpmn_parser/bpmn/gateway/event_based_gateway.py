"""Definitions for the bpmn:eventBasedGateway XML element."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.bpmn.types import EventBasedGatewayType
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class EventBasedGateway(Gateway):
    """The Event-Based Gateway represents a branching point in the Process based on Events that occur."""

    class Meta:
        name = "eventBasedGateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    instantiate: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    event_gateway_type: EventBasedGatewayType = field(
        default=EventBasedGatewayType.EXCLUSIVE,
        metadata={
            "name": "eventGatewayType",
            "type": "Attribute",
        },
    )
