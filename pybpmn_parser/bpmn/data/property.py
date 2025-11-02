"""Represents a Property."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.data_state import DataState


@register_element
@dataclass(kw_only=True)
class Property(BaseElement):
    """
    Properties are item-aware bpmn not visually displayed on a Process diagram.

    Only Processes, Activities, and Events may contain Properties.
    """

    data_state: Optional[DataState] = field(
        default=None,
        metadata={
            "name": "dataState",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to the DataState, which defines certain states for the data contained in the Property."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """Defines the name of the Property."""

    item_subject_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "itemSubjectRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """Specification of the items that are stored in the Property."""

    class Meta:
        name = "property"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Property]:
        """Parse the given XML element."""
        from pybpmn_parser.bpmn.data.data_state import DataState

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "item_subject_ref": obj.get("itemSubjectRef"),
                "data_state": DataState.parse(obj.find("./bpmn:dataState", NAMESPACES)),
            }
        )
        return cls(**attribs)
