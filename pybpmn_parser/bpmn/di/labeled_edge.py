"""Model definitions for labeled edges."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.di.edge import Edge

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class LabeledEdge(Edge):
    """A LabeledEdge represents an edge that owns a collection of labels."""

    class Meta:
        name = "labeledEdge"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"
