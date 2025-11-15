"""Represents an Association."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.common.artifact import Artifact
from pybpmn_parser.bpmn.types import AssociationDirection
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Association(Artifact):
    """An Association is used to associate information and Artifacts with Flow Objects."""

    source_ref: str = field(
        metadata={
            "name": "sourceRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    """The IDREF that the Association is connecting from."""

    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    """The IDREF that the Association is connecting to."""

    association_direction: AssociationDirection = field(
        default=AssociationDirection.NONE,
        metadata={
            "name": "associationDirection",
            "type": "Attribute",
        },
    )
    """Defines whether the Association shows any directionality with an arrowhead.
    The default is None (no arrowhead). A value of One means that the arrowhead will be at the Target Object.
    A value of Both means that there will be an arrowhead at both ends of the Association line."""

    class Meta:
        name = "association"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
