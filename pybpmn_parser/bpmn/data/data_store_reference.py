"""Represents a BPMN 2.0 data store reference."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.data_state import DataState


@dataclass(kw_only=True)
class DataStoreReference(FlowElement):
    """A reference to a data store."""

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
    data_store_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataStoreRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[DataStoreReference]:
        """Parse the given XML element."""
        from pybpmn_parser.bpmn.data.data_state import DataState

        if obj is None:
            return None

        baseclass = FlowElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "item_subject_ref": obj.get("itemSubjectRef"),
                "data_store_ref": obj.get("dataStoreRef"),
                "data_state": DataState.parse(obj.find("./bpmn:dataState", NAMESPACES)),
            }
        )

        return cls(**attribs)
