"""Representation of a BPMN Lane."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@dataclass(kw_only=True)
class BaseLane(BaseElement):
    """BaseLane is the abstract super class for Lane."""

    partition_element: Optional[BaseElement] = field(
        default=None,
        metadata={
            "name": "partitionElement",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A BaseElement that specifies the partition value and partition type.

    Using this partition element, a BPMN-compliant tool can determine the FlowElements that have to be
    partitioned in this Lane."""

    flow_node_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "flowNodeRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """The list of FlowNodes is partitioned into this Lane according to the partition_element."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The name of the Lane."""

    partition_element_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "partitionElementRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """A reference to a BaseElement that specifies the partition value and partition type.

    Using this partition element, a BPMN-compliant tool can determine the FlowElements that have to be
    partitioned in this Lane."""


@dataclass(kw_only=True)
class EmbeddedLaneSet(BaseElement):
    """The LaneSet element defines the container for one or more Lanes."""

    lane: list[BaseLane] = field(
        default_factory=list,
        metadata={
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


@register_element
@dataclass(kw_only=True)
class Lane(BaseLane):
    """A Lane is a subpartition within a Process and will extend the entire length of the Process."""

    child_lane_set: Optional[EmbeddedLaneSet] = field(
        default=None,
        metadata={
            "name": "childLaneSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to a LaneSet element for embedded Lanes."""

    class Meta:
        name = "lane"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class LaneSet(EmbeddedLaneSet):
    """The LaneSet element defines the container for one or more Lanes."""

    class Meta:
        name = "laneSet"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    lane: list[Lane] = field(  # type: ignore[assignment]
        default_factory=list,
        metadata={
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
