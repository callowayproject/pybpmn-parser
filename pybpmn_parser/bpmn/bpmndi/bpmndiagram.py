"""Model definitions for BPMNDiagram."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.di.diagram import Diagram
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.bpmndi.bpmnlabel_style import BPMNLabelStyle
    from pybpmn_parser.bpmn.bpmndi.bpmnplane import BPMNPlane

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNDiagram(Diagram):
    """A `BPMNDiagram` is a diagram that depicts all or part of a BPMN model."""

    class Meta:
        name = "BPMNDiagram"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    plane: BPMNPlane = field(
        metadata={
            "name": "BPMNPlane",
            "type": "Element",
            "required": True,
        }
    )
    """A BPMN plane element that is the container of all diagram elements in this diagram."""

    label_styles: list[BPMNLabelStyle] = field(
        default_factory=list,
        metadata={
            "name": "BPMNLabelStyle",
            "type": "Element",
        },
    )
    """A collection of BPMN label styles that are owned by the diagram and referenced by label elements."""
