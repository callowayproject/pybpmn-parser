"""Represents a Data Output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.data_state import DataState


@register_element
@dataclass(kw_only=True)
class DataOutput(BaseElement):
    """A Data Output is a declaration that a particular kind of data will be used as output of the ioSpecification."""

    data_state: Optional[DataState] = field(
        default=None,
        metadata={
            "name": "dataState",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to the DataState, which defines certain states for the data contained in the Item."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """A descriptive name for the data output."""

    item_subject_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "itemSubjectRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """Specification of the items that are stored by the DataOutput."""

    is_collection: bool = field(
        default=False,
        metadata={
            "name": "isCollection",
            "type": "Attribute",
        },
    )
    """Defines if the DataOutput represents a collection of elements.

    It is necessary when `item_subject_ref` is `None`.

    If `item_subject_ref` is not `None`, then this attribute MUST have the same value as the `is_collection` attribute
    of the referenced `item_subject_ref`. The default value for this attribute is false."""

    class Meta:
        name = "dataOutput"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
