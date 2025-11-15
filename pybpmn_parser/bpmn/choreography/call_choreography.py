"""Represents a Choreography Task that calls another Choreography."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.choreography.choreography_activity import ChoreographyActivity
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation


@register_element
@dataclass(kw_only=True)
class CallChoreography(ChoreographyActivity):
    """A Call Choreography identifies a point in the Process where a Choreography or a Choreography Task is used."""

    participant_associations: list[ParticipantAssociation] = field(
        default_factory=list,
        metadata={
            "name": "participantAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    called_choreography_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "calledChoreographyRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "callChoreography"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
