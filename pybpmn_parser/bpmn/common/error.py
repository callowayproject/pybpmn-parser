"""Represents an Error."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class Error(RootElement):
    """An Error represents the content of an Error Event or the Fault of a failed Operation."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    error_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorCode",
            "type": "Attribute",
        },
    )
    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Error]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = RootElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "error_code": obj.get("errorCode"),
                "structure_ref": obj.get("structureRef"),
            }
        )
        return cls(**attribs)
