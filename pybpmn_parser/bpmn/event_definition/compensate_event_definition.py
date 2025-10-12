"""Represents a Compensate Event Definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition import EventDefinition

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class CompensateEventDefinition(EventDefinition):
    """The definition of a CompensateEvent."""

    wait_for_completion: bool = field(
        default=True,
        metadata={
            "name": "waitForCompletion",
            "type": "Attribute",
        },
    )
    activity_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "activityRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CompensateEventDefinition]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "wait_for_completion": obj.get("waitForCompletion", True),
                "activity_ref": obj.get("activityRef"),
            }
        )
        return cls(**attribs)
