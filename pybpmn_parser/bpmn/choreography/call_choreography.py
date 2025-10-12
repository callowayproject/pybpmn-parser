"""Represents a Choreography Task that calls another Choreography."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.choreography.choreography_activity import ChoreographyActivity
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CallChoreography]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.collaboration.participant_association import ParticipantAssociation

        if obj is None:
            return None

        baseclass = ChoreographyActivity.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "called_choreography_ref": obj.get("calledChoreographyRef"),
                "participant_associations": [
                    ParticipantAssociation.parse(elem)
                    for elem in obj.findall("./bpmn:participantAssociation", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
