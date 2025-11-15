"""Representation of an Event."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.common.flow_node import FlowNode
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.property import Property


@register_element
@dataclass(kw_only=True)
class Event(FlowNode):  # Is Abstract
    """The Event element is used to define an event in a BPMN 2.0 process model."""

    properties: list[Property] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Modeler-defined properties of this event."""

    class Meta:
        name = "event"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
