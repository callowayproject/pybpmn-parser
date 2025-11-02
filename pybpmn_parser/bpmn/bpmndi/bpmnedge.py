"""Model definitions for BPMN edges."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.di.labeled_edge import LabeledEdge
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.bpmndi.bpmnlabel import BPMNLabel
    from pybpmn_parser.bpmn.bpmndi.types import MessageVisibleKind

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNEdge(LabeledEdge):
    """A BPMNEdge is an edge that depicts a relationship between two BPMN model elements."""

    class Meta:
        name = "BPMNEdge"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    label: Optional[BPMNLabel] = field(
        default=None,
        metadata={
            "name": "BPMNLabel",
            "type": "Element",
        },
    )
    """An optional label that is nested when the edge has a visible text label with its own bounding box."""

    bpmn_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "bpmnElement",
            "type": "Attribute",
        },
    )
    """A reference to a connecting BPMN element that this edge depicts."""

    source_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "sourceElement",
            "type": "Attribute",
        },
    )
    """An optional reference to the edge's source element if different from the source inferred from bpmn_element."""

    target_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "targetElement",
            "type": "Attribute",
        },
    )
    """
    An optional reference to the edge's target element if different from the target inferred from the bpmn_element.
    """

    message_visible_kind: Optional[MessageVisibleKind] = field(
        default=None,
        metadata={
            "name": "messageVisibleKind",
            "type": "Attribute",
        },
    )
    """An optional attribute that should be used only for Message Flow."""
