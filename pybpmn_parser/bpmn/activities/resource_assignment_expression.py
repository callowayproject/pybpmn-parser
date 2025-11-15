"""Represents a Resource Assignment Expression."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression, FormalExpression


@register_element
@dataclass(kw_only=True)
class ResourceAssignmentExpression(BaseElement):
    """This defines the Expression used for the Resource assignment."""

    formal_expression: Optional[FormalExpression] = field(
        default=None,
        metadata={
            "name": "formalExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    expression: Optional[Expression] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    class Meta:
        name = "resourceAssignmentExpression"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
