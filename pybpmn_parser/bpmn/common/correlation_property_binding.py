"""Represents a Correlation Property Binding."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import FormalExpression


@register_element
@dataclass(kw_only=True)
class CorrelationPropertyBinding(BaseElement):
    """
    CorrelationPropertyBindings represent the partial keys of a CorrelationSubscription.

    Each relates to a specific CorrelationProperty in the associated CorrelationKey.
    A FormalExpression defines how that CorrelationProperty instance is populated and updated at runtime from the
    Process context (i.e., its Data Objects and Properties).
    """

    data_path: FormalExpression = field(
        metadata={
            "name": "dataPath",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    correlation_property_ref: str = field(
        metadata={
            "name": "correlationPropertyRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "correlationPropertyBinding"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CorrelationPropertyBinding]:
        """Parse an XML object into a CorrelationPropertyBinding object."""
        from pybpmn_parser.bpmn.common.expression import FormalExpression

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "correlation_property_ref": obj.get("correlationPropertyRef"),
                "data_path": FormalExpression.parse(obj.find("./bpmn:dataPath", NAMESPACES)),
            }
        )
        return cls(**attribs)
