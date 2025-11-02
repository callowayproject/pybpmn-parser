"""Represents a Correlation Subscription."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.correlation_property_binding import CorrelationPropertyBinding


@register_element
@dataclass(kw_only=True)
class CorrelationSubscription(BaseElement):
    """A CorrelationSubscription acts as the Process-specific counterpart to a specific CorrelationKey."""

    correlation_property_bindings: list[CorrelationPropertyBinding] = field(
        default_factory=list,
        metadata={
            "name": "correlationPropertyBinding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    correlation_key_ref: str = field(
        metadata={
            "name": "correlationKeyRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "correlationSubscription"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CorrelationSubscription]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.common.correlation_property_binding import CorrelationPropertyBinding

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "correlation_property_bindings": [
                    CorrelationPropertyBinding.parse(elem) for elem in obj.findall("./bpmn:correlationPropertyBinding")
                ],
                "correlation_key_ref": obj.get("correlationKeyRef", ""),
            }
        )
        return cls(**attribs)
