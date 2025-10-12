"""Represents a Send Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class SendTask(Task):
    """A Send Task is a simple Task that is designed to send a Message to an external Participant."""

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.WEB_SERVICE,
        metadata={
            "type": "Attribute",
        },
    )
    message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageRef",
            "type": "Attribute",
        },
    )
    operation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationRef",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[SendTask]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = Task.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.WEB_SERVICE),
                "message_ref": obj.get("messageRef"),
                "operation_ref": obj.get("operationRef"),
            }
        )

        return cls(**attribs)
