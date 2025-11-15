"""Represents a Global Choreography Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.choreography.choreography import Choreography
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class GlobalChoreographyTask(Choreography):
    """A GlobalChoreographyTask is a reusable Choreography Task definition callable from within any Choreography."""

    initiating_participant_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "initiatingParticipantRef",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "globalChoreographyTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
