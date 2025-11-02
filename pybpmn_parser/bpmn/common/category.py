"""Representation of a BPMN category."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement, RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CategoryValue]:
        """Parse xml into this class."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "value": obj.get("value"),
            }
        )

        return cls(**attribs)


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Category]:
        """Parse an XML element into a Category object."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "category_value": [
                    CategoryValue.parse(elem) for elem in obj.findall("./bpmn:categoryValue", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
