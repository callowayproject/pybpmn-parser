"""Represents a Group."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.artifact import Artifact

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class Group(Artifact):
    """Groups are often used to highlight certain subclauses of a Diagram without adding additional constraints."""

    category_value_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "categoryValueRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Group]:
        """Parse the given XML element."""
        if obj is None:
            return None

        baseclass = Artifact.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "category_value_ref": obj.get("categoryValueRef"),
            }
        )
        return cls(**attribs)
