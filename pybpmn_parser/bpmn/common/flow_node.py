"""Represents a FlowNode."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class FlowNode(FlowElement):  # Is Abstract
    """The FlowNode element is used to provide a single element as the source and target Sequence Flow associations."""

    incoming: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    outgoing: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )

    class Meta:
        name = "flowNode"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
