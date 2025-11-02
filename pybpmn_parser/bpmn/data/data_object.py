"""Represents a Data Object."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import strtobool
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.data_state import DataState


@register_element
@dataclass(kw_only=True)
class DataObject(FlowElement):
    """The primary construct for modeling data within the Process flow."""

    data_state: Optional[DataState] = field(
        default=None,
        metadata={
            "name": "dataState",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
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
    is_collection: bool = field(
        default=False,
        metadata={
            "name": "isCollection",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "dataObject"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[DataObject]:
        """Parse the given XML element."""
        from pybpmn_parser.bpmn.data.data_state import DataState

        if obj is None:
            return None

        baseclass = FlowElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "item_subject_ref": obj.get("itemSubjectRef"),
                "is_collection": strtobool(obj.get("isCollection", "false")),
                "data_state": DataState.parse(obj.find("./bpmn:dataState", NAMESPACES)),
            }
        )
        return cls(**attribs)
