"""Model definitions for BPMN Plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.di.plane import Plane
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.bpmndi.bpmnedge import BPMNEdge
    from pybpmn_parser.bpmn.bpmndi.bpmnshape import BPMNShape

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNPlane(Plane):
    """A BPMNPlane is the BPMNDiagram container of BPMNShape and BPMNEdge."""

    class Meta:
        name = "BPMNPlane"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    bpmn_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "bpmnElement",
            "type": "Attribute",
        },
    )
    """
    A reference to a Process, SubProcess, AdHocSubProcess, Transaction, Collaboration, Choreography, or SubChoreography
    in a BPMN model.
    """

    bpmn_shapes: list[BPMNShape] = field(
        default_factory=list,
        metadata={"name": "BPMNShape", "type": "Element", "namespace": "http://www.omg.org/spec/BPMN/20100524/DI"},
    )
    """A reference to a BPMNShape element."""

    bpmn_edges: list[BPMNEdge] = field(
        default_factory=list,
        metadata={"name": "BPMNEdge", "type": "Element", "namespace": "http://www.omg.org/spec/BPMN/20100524/DI"},
    )
    """A reference to a BPMNEdge element."""
