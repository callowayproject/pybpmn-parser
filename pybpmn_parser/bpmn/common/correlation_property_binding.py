"""Represents a Correlation Property Binding."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
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
