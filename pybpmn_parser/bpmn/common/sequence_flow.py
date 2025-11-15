"""Represents a Sequence Flow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class SequenceFlow(FlowElement):
    """The Sequence Flow element is used to define the sequence of execution between two FlowNodes."""

    condition_expression: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "conditionExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    source_ref: str = field(
        metadata={
            "name": "sourceRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    is_immediate: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isImmediate",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "sequenceFlow"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
