"""Represents a Complex Behavior Definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import FormalExpression
    from pybpmn_parser.bpmn.event.implicit_throw_event import ImplicitThrowEvent


@register_element
@dataclass(kw_only=True)
class ComplexBehaviorDefinition(BaseElement):
    """
    This controls when and which Events are thrown if the behavior of the Multi-Instance Activity is set to complex.
    """

    condition: FormalExpression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    event: Optional[ImplicitThrowEvent] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    class Meta:
        name = "complexBehaviorDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
