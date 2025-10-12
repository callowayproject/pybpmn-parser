"""Represents a signal event definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition import EventDefinition

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class SignalEventDefinition(EventDefinition):
    """The definition of a Signal event."""

    signal_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "signalRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[EventDefinition]:
        """Parse an XML element into this class."""
        if obj is None:
            return None

        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "signal_ref": obj.get("signalRef"),
            }
        )
        return cls(**attribs)
