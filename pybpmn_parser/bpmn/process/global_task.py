"""Represents a Global Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.common.callable_element import CallableElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
    from pybpmn_parser.bpmn.process.performer import HumanPerformer, Performer, PotentialOwner


@register_element
@dataclass(kw_only=True)
class GlobalTask(CallableElement):
    """A Global Task is a reusable, Task definition that can be called from within any Process by a Call Activity."""

    potential_owners: list[PotentialOwner] = field(
        default_factory=list,
        metadata={
            "name": "potentialOwner",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Potential owners of a User Task are persons who can claim and work on it."""

    human_performers: list[HumanPerformer] = field(
        default_factory=list,
        metadata={
            "name": "humanPerformer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    performers: list[Performer] = field(
        default_factory=list,
        metadata={
            "name": "performer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    resources: list[ResourceRole] = field(
        default_factory=list,
        metadata={
            "name": "resourceRole",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Defines the resource that will perform or will be responsible for the Activity.

    The resource, e.g., a performer, can be specified in the form of a specific individual, a group, an organization
    role or position, or an organization."""

    class Meta:
        name = "globalTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
