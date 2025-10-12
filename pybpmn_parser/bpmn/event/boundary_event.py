"""Represents a boundary event."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event.catch_event import CatchEvent
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class BoundaryEvent(CatchEvent):
    """The Boundary Event is a special kind of Catch Event that is attached to a specific Activity."""

    cancel_activity: bool = field(
        default=True,
        metadata={
            "name": "cancelActivity",
            "type": "Attribute",
        },
    )
    attached_to_ref: str = field(
        metadata={
            "name": "attachedToRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[BoundaryEvent]:
        """Parse xml into this class."""
        if obj is None:
            return None

        baseclass = CatchEvent.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "cancel_activity": strtobool(obj.get("cancelActivity")),
                "attached_to_ref": obj.get("attachedToRef"),
            }
        )
        return cls(**attribs)
