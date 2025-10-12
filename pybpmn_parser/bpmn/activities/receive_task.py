"""Represents a Receive Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ReceiveTask(Task):
    """A ReceiveTask is a simple Task designed to wait for a Message to arrive from an external Participant."""

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.WEB_SERVICE,
        metadata={
            "type": "Attribute",
        },
    )
    instantiate: bool = field(
        default=False,
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
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ReceiveTask]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = Task.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attributes.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.WEB_SERVICE),
                "instantiate": strtobool(obj.get("instantiate", "false")),
                "message_ref": obj.get("messageRef"),
                "operation_ref": obj.get("operationRef"),
            }
        )

        return cls(**attributes)
