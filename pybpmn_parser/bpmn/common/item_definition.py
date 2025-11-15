"""Definitions for the bpmn:itemDefinition XML element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import ItemKind
from pybpmn_parser.element_registry import register_element


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
