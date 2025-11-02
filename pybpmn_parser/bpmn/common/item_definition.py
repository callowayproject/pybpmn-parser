"""Definitions for the bpmn:itemDefinition XML element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import ItemKind
from pybpmn_parser.core import strtobool
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class ItemDefinition(RootElement):
    """An ItemDefinition can specify an import reference where the proper definition of the structure is defined."""

    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
        },
    )
    is_collection: bool = field(
        default=False,
        metadata={
            "name": "isCollection",
            "type": "Attribute",
        },
    )
    item_kind: ItemKind = field(
        default=ItemKind.INFORMATION,
        metadata={
            "name": "itemKind",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "itemDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ItemDefinition]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "structure_ref": obj.get("structureRef"),
                "is_collection": strtobool(obj.get("isCollection", "false")),
                "item_kind": obj.get("itemKind"),
            }
        )
        return cls(**attribs)
