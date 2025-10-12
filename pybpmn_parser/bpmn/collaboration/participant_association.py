"""Represents a Participant Association."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ParticipantAssociation(BaseElement):
    """A ParticipantAssociation is used to map between two bpmn that both contain Participants."""

    inner_participant_ref: str = field(
        metadata={
            "name": "innerParticipantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
            "is_reference": True,
        }
    )
    outer_participant_ref: str = field(
        metadata={
            "name": "outerParticipantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
            "is_reference": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ParticipantAssociation]:
        """Parse an XML object into a ParticipantAssociation object."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "inner_participant_ref": obj.find("./bpmn:innerParticipantRef", NAMESPACES).text,
                "outer_participant_ref": obj.find("./bpmn:outerParticipantRef", NAMESPACES).text,
            }
        )
        return cls(**attribs)
