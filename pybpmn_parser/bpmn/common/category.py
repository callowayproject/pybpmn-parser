"""Representation of a BPMN category."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement, RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class CategoryValue(BaseElement):
    """
    The categoryValue attribute specifies one or more values of the Category.

    For example, the Category is "Region" then this Category could specify values like
    "North," "South," "West," and "East."
    """

    class Meta:
        name = "categoryValue"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@register_element
@dataclass(kw_only=True)
class Category(RootElement):
    """Categories, which have user-defined semantics, can be used for documentation or analysis."""

    category_value: list[CategoryValue] = field(
        default_factory=list,
        metadata={
            "name": "categoryValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "category"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
