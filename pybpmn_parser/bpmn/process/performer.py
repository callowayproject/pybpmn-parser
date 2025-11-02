"""Representations of Performer bpmn."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Performer(ResourceRole):
    """
    The Performer class defines the resource that will perform or will be responsible for an Activity.

    The performer can be specified in the form of a specific individual, a group, an organization role or position,
    or an organization.
    """

    class Meta:
        name = "performer"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class HumanPerformer(Performer):
    """Person assigned to an Activity."""

    class Meta:
        name = "humanPerformer"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class PotentialOwner(HumanPerformer):
    """
    Potential owners of a User Task are persons who can claim and work on it.

    A potential owner becomes the actual owner of a Task, usually by explicitly claiming it.
    """

    class Meta:
        name = "potentialOwner"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
