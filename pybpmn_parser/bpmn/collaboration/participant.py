"""Represents a Participant."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement, RootElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.collaboration.participant_multiplicity import ParticipantMultiplicity


@register_element
@dataclass(kw_only=True)
class Participant(BaseElement):
    """A Participant is a specific or general participant in a Collaboration."""

    interface_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "interfaceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    end_point_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "endPointRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    participant_multiplicity: Optional[ParticipantMultiplicity] = field(
        default=None,
        metadata={
            "name": "participantMultiplicity",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    process_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "processRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "participant"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Participant]:
        """Parse an XML element into a Participant object."""
        from pybpmn_parser.bpmn.collaboration.participant_multiplicity import ParticipantMultiplicity

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "process_ref": obj.get("processRef"),
                "interface_refs": [elem.text for elem in obj.findall("./bpmn:interfaceRef", NAMESPACES)],
                "end_point_refs": [elem.text for elem in obj.findall("./bpmn:endPointRef", NAMESPACES)],
                "participant_multiplicity": ParticipantMultiplicity.parse(
                    obj.find("./bpmn:participantMultiplicity", NAMESPACES)
                ),
            }
        )

        return cls(**attribs)


@dataclass(kw_only=True)
class PartnerEntity(RootElement):
    """A PartnerEntity is a specific participant (e.g., a company)."""

    participant_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "participantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[PartnerEntity]:
        """Parse an XML element into a PartnerEntity object."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {"name": obj.get("name"), "participant_refs": [elem.text for elem in obj.findall("./bpmn:participantRef")]}
        )
        return cls(**attribs)


@dataclass(kw_only=True)
class PartnerRole(RootElement):
    """A PartnerRole is general participant (e.g., a buyer, seller, or manufacturer)."""

    participant_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "participantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[PartnerRole]:
        """Parse an XML element into a PartnerRole object."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "participant_refs": [elem.text for elem in obj.findall("./bpmn:participantRef", NAMESPACES)],
            }
        )
        return cls(**attribs)
