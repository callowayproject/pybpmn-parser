"""Represents a Data State."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class DataState(BaseElement):
    """The state of the data contained in the Data Object."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "dataState"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[DataState]:
        """Parse xml into this class."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attributes["name"] = obj.get("name")
        return cls(**attributes)
