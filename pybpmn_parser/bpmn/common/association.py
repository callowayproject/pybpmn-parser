"""Represents an Association."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.artifact import Artifact
from pybpmn_parser.bpmn.types import AssociationDirection

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Association]:
        """Parse the given XML element."""
        if obj is None:
            return None

        baseclass = Artifact.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "source_ref": obj.get("sourceRef"),
                "target_ref": obj.get("targetRef"),
                "association_direction": obj.get("associationDirection", AssociationDirection.NONE),
            }
        )

        return cls(**attribs)
