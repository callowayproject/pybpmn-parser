"""Represents a Global Choreography Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.choreography.choreography import Choreography

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[GlobalChoreographyTask]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = Choreography.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "initiating_participant_ref": obj.get("initiatingParticipantRef"),
            }
        )
        return cls(**attribs)
