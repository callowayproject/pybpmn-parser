"""Represents a Call Activity."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.activity import Activity
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class CallActivity(Activity):
    """The Call Activity acts as a 'wrapper' for the invocation of a global Process or Task within the execution."""

    called_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "calledElement",
            "type": "Attribute",
        },
    )
    """The element to be called, which will be either a Process or a GlobalTask."""

    class Meta:
        name = "callActivity"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CallActivity]:
        """Parse XML into this class."""
        if obj is None:
            return None

        baseclass = Activity.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update({"called_element": obj.get("calledElement")})

        return cls(**attribs)
