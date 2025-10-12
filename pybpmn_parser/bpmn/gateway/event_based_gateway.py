"""Definitions for the bpmn:eventBasedGateway XML element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.bpmn.types import EventBasedGatewayType
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class EventBasedGateway(Gateway):
    """The Event-Based Gateway represents a branching point in the Process based on Events that occur."""

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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[EventBasedGateway]:
        """Parse the given XML element."""
        if obj is None:
            return None
        baseclass = Gateway.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "instantiate": strtobool(obj.get("instantiate", "false")),
                "event_gateway_type": obj.get("eventGatewayType"),
            }
        )
        return cls(**attribs)
