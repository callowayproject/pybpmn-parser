"""Represents an error event definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition import EventDefinition

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ErrorEventDefinition(EventDefinition):
    """The definition of an error event."""

    error_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ErrorEventDefinition]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "error_ref": obj.get("errorRef"),
            }
        )
        return cls(**attribs)
