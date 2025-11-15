"""Represents a BPMN 2.0 complex gateway."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class ComplexGateway(Gateway):
    """The Complex Gateway can be used to model complex synchronization behavior."""

    class Meta:
        name = "complexGateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    activation_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "activationCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Determines which combination of incoming tokens will be synchronized for activation of the Gateway."""

    default: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """The Sequence Flow that receives a token when all other Sequence Flows' conditions evaluate to false."""
