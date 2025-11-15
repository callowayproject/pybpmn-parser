"""Represents a BPMN 2.0 exclusive gateway."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ExclusiveGateway(Gateway):
    """A diverging Exclusive Gateway is used to create alternative paths within a Process flow."""

    class Meta:
        name = "exclusiveGateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    default: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """The Sequence Flow that receives a token when all other Sequence Flows' conditions evaluate to false."""
