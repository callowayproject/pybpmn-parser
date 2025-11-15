"""Represents a Data Association."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import FormalExpression
    from pybpmn_parser.bpmn.data.assignment import Assignment


@register_element
@dataclass(kw_only=True)
class DataAssociation(BaseElement):
    """
    Data Associations move data between Data Objects/Properties, and inputs/outputs of Activities/Processes/etc.
    """

    source_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "sourceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
            "is_reference": True,
        }
    )
    transformation: Optional[FormalExpression] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    assignments: list[Assignment] = field(
        default_factory=list,
        metadata={
            "name": "assignment",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    class Meta:
        name = "dataAssociation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@dataclass(kw_only=True)
class DataOutputAssociation(DataAssociation):
    """DataOutputAssociation is used to model how data is pulled from item-aware bpmn."""

    pass


@dataclass(kw_only=True)
class DataInputAssociation(DataAssociation):
    """DataInputAssociation is used to model how data is pushed into item-aware bpmn."""

    pass
