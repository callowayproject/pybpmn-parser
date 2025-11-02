"""Represents a BPMN 2.0 inclusive gateway."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class InclusiveGateway(Gateway):
    """An Inclusive Gateway can be used to create alternative but also parallel paths within a Process flow."""

    class Meta:
        name = "inclusiveGateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    default: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """The Sequence Flow that receives a token when all other Sequence Flows' conditions evaluate to false."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[InclusiveGateway]:
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
