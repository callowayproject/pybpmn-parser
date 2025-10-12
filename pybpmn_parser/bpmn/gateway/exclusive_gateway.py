"""Represents a BPMN 2.0 exclusive gateway."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.gateway import Gateway

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ExclusiveGateway(Gateway):
    """A diverging Exclusive Gateway is used to create alternative paths within a Process flow."""

    default: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """The Sequence Flow that receives a token when all other Sequence Flows' conditions evaluate to false."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ExclusiveGateway]:
        """Parse the given XML element."""
        if obj is None:
            return None

        baseclass = Gateway.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "default": obj.get("default"),
            }
        )

        return cls(**attribs)
