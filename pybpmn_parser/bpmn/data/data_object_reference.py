"""Represents a BPMN 2.0 data object reference."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.data_state import DataState


@register_element
@dataclass(kw_only=True)
class DataObjectReference(FlowElement):
    """A reference to a data object."""

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
    data_object_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataObjectRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "dataObjectReference"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
