"""Represents a DataStore."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import strtobool
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.data_state import DataState


@register_element
@dataclass(kw_only=True)
class DataStore(RootElement):
    """A DataStore provides a mechanism for Activities to retrieve or update stored information that will persist."""

    data_state: Optional[DataState] = field(
        default=None,
        metadata={
            "name": "dataState",
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
    capacity: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_unlimited: bool = field(
        default=True,
        metadata={
            "name": "isUnlimited",
            "type": "Attribute",
        },
    )
    item_subject_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "itemSubjectRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "dataStore"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[DataStore]:
        """Parse the given XML element."""
        from pybpmn_parser.bpmn.data.data_state import DataState

        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "capacity": obj.get("capacity"),
                "is_unlimited": strtobool(obj.get("isUnlimited", "false")),
                "item_subject_ref": obj.get("itemSubjectRef"),
                "data_state": DataState.parse(obj.find("./bpmn:dataState", NAMESPACES)),
            }
        )

        return cls(**attribs)
