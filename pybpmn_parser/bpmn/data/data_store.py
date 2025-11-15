"""Represents a DataStore."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
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
