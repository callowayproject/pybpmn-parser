"""Model definition for Edge."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.dc.point import Point
from pybpmn_parser.bpmn.di.diagram_element import DiagramElement
from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"


@register_element
@dataclass(kw_only=True)
class Waypoint(Point):
    """A waypoint represents a point on an edge."""

    class Meta:
        name = "waypoint"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"


@register_element
@dataclass(kw_only=True)
class Edge(DiagramElement):
    """Edge specifies a polyline connection between two graph elements: a source and a target."""

    class Meta:
        name = "edge"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    waypoint: list[Waypoint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/DD/20100524/DI",
            "min_occurs": 2,
        },
    )
    """A list of two or more points that specifies the connected line segments of the edge."""
