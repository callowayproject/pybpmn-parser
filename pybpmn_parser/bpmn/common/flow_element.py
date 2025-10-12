"""Represents a BPMN Flow Element."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    import lxml.etree as ET

    from pybpmn_parser.bpmn.process.auditing import Auditing
    from pybpmn_parser.bpmn.process.monitoring import Monitoring


@dataclass(kw_only=True)
class FlowElement(BaseElement):  # Is Abstract
    """FlowElement is the abstract super class for all bpmn that can appear in a Process flow."""

    auditing: Optional[Auditing] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    monitoring: Optional[Monitoring] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    category_value_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "categoryValueRef",
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
    def parse(cls, obj: Optional[ET.Element]) -> Optional[FlowElement]:
        """Parse an object into this element."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "auditing": obj.find("./bpmn:auditing", NAMESPACES),
                "monitoring": obj.find("./bpmn:monitoring", NAMESPACES),
                "category_value_refs": [elem.text for elem in obj.findall("./bpmn:categoryValueRef", NAMESPACES)],
            }
        )
        return cls(**attribs)
