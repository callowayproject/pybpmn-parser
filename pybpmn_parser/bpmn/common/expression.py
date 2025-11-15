"""Represents an Expression."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Expression(BaseElement):  # Is Abstract
    """The Expression class is used to specify an Expression using natural-language text."""

    value: Optional[str] = field(default=None, metadata={"name": "#text", "type": "Attribute"})

    class Meta:
        name = "expression"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class FormalExpression(Expression):
    """The FormalExpression class is used to specify an executable Expression using a specified Expression language."""

    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    evaluates_to_type_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "evaluatesToTypeRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "formalExpression"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
