"""Represents a Receive Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ReceiveTask(Task):
    """A ReceiveTask is a simple Task designed to wait for a Message to arrive from an external Participant."""

    implementation: ImplementationValue = field(
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

    class Meta:
        name = "receiveTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
