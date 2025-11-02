"""Represents a BPMN signal element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class Signal(RootElement):
    """
    Signals are triggers generated in the Pool they are published.

    They are typically used for broadcast communication within and across Processes, across Pools, and
    between Process diagrams.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "signal"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Signal]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "structure_ref": obj.get("structureRef"),
            }
        )
        return cls(**attribs)
