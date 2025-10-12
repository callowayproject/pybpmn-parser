"""Represents a Resource Parameter."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ResourceParameter(BaseElement):
    """A parameter for a resource used at runtime to define a query e.g., into an Organizational Directory."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    is_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isRequired",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ResourceParameter]:
        """Parse an XML element into a ResourceParameter object."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        is_required = obj.get("isRequired")
        attribs.update(
            {
                "name": obj.get("name"),
                "type_value": obj.get("type"),
                "is_required": strtobool(is_required) if is_required else None,
            }
        )
        return cls(**attribs)
