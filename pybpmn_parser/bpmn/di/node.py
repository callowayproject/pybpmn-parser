"""Model definition for a Node."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.di.diagram_element import DiagramElement

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Node(DiagramElement):
    """Node specifies a given node in a graph of diagram elements."""

    class Meta:
        name = "node"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"
