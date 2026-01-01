"""Represents a User Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.rendering import Rendering


@register_element
@dataclass(kw_only=True)
class UserTask(Task):
    """
    A User Task is a workflow Task where a human performer performs the Task with the assistance of a software app.

    The lifecycle of the Task is managed by a software component (called activities manager) and is typically executed
    in the context of a Process.
    """

    renderings: list[Rendering] = field(
        default_factory=list,
        metadata={
            "name": "rendering",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A hook that enables BPMN adopters to specify task rendering attributes using the BPMN Extension mechanism."""

    implementation: ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute specifies the technology to be used for implementing the User Task.

    Valid values are "##unspecified" for leaving the implementation technology open,
    "##WebService" for the Web service technology, or a URI identifying any other technology or coordination protocol.
    The default technology for this task is unspecified."""

    class Meta:
        name = "userTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
