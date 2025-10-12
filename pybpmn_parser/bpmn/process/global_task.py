"""Represents a Global Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.callable_element import CallableElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
    from pybpmn_parser.bpmn.process.performer import HumanPerformer, Performer, PotentialOwner


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[GlobalTask]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
        from pybpmn_parser.bpmn.process.performer import HumanPerformer, Performer, PotentialOwner

        if obj is None:
            return None

        baseclass = CallableElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "human_performers": [
                    HumanPerformer.parse(elem) for elem in obj.findall("./bpmn:humanPerformer", NAMESPACES)
                ],
                "performers": [Performer.parse(elem) for elem in obj.findall("./bpmn:performer", NAMESPACES)],
                "potential_owners": [
                    PotentialOwner.parse(elem) for elem in obj.findall("./bpmn:potentialOwner", NAMESPACES)
                ],
                "resources": [ResourceRole.parse(elem) for elem in obj.findall("./bpmn:resourceRole", NAMESPACES)],
            }
        )
        return cls(**attribs)
