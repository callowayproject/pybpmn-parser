"""Represents a BPMN 2.0 Participant Multiplicity element."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ParticipantMultiplicity(BaseElement):
    """The Participant Multiplicity specifies the number of Participant instances that can be concurrently active."""

    minimum: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    maximum: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "participantMultiplicity"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
