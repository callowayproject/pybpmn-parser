"""Model definition for Plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.di.node import Node
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.di.diagram_element import DiagramElement

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"


@register_element
@dataclass(kw_only=True)
class Plane(Node):
    """
    A plane is a node with infinite bounds with a collection of shapes and edges laid out relative to its origin point.
    """

    class Meta:
        name = "plane"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    diagram_elements: list[DiagramElement] = field(
        default_factory=list,
        metadata={
            "name": "diagramElement",
            "type": "Element",
        },
    )
