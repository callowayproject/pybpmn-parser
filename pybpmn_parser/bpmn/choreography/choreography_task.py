"""Represents a Choreography Task."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.choreography.choreography_activity import ChoreographyActivity
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ChoreographyTask(ChoreographyActivity):
    """
    A Choreography Task is an atomic Activity in a Choreography Process.

    It represents an Interaction, which is one or two Message exchanges between two Participants.
    """

    message_flow_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "messageFlowRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )

    class Meta:
        name = "choreographyTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
