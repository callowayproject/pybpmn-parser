"""Representation of a BPMN Lane."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional

import lxml.etree as ET
import xmltodict

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES


@dataclass(kw_only=True)
class Lane(BaseElement):
    """A Lane is a subpartition within a Process and will extend the entire length of the Process."""

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

    child_lane_set: Optional[LaneSet] = field(
        default=None,
        metadata={
            "name": "childLaneSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to a LaneSet element for embedded Lanes."""

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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Lane]:
        """Parse a Lane XML element into a Lane object."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        partition_element = obj.find("./bpmn:partitionElement", NAMESPACES)

        attribs.update(
            {
                "name": obj.get("name"),
                "partition_element_ref": obj.get("partitionElementRef"),
                "partition_element": xmltodict.parse(ET.tostring(partition_element))
                if partition_element is not None
                else None,
                "flow_node_refs": [elem.text for elem in obj.findall("./bpmn:flowNodeRef", NAMESPACES)],
                "child_lane_set": LaneSet.parse(obj.find("./bpmn:childLaneSet", NAMESPACES)),
            }
        )
        return cls(**attribs)


@dataclass(kw_only=True)
class LaneSet(BaseElement):
    """The LaneSet element defines the container for one or more Lanes."""

    lane: list[Lane] = field(
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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[LaneSet]:
        """Parse a LaneSet XML element into a LaneSet object."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "lane": [Lane.parse(elem) for elem in obj.findall("./bpmn:lane", NAMESPACES)],
            }
        )

        return cls(**attribs)
