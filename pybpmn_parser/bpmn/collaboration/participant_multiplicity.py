"""Represents a BPMN 2.0 Participant Multiplicity element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ParticipantMultiplicity]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "minimum": int(obj.get("minimum", 0)),
                "maximum": int(obj.get("maximum", 1)),
            }
        )
        return cls(**attribs)
