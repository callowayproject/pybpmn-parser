"""The binding of a resource parameter to a formal expression."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression, FormalExpression


@register_element
@dataclass(kw_only=True)
class ResourceParameterBinding(BaseElement):
    """The binding of a resource parameter to a formal expression."""

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
    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "resourceParameterBinding"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
