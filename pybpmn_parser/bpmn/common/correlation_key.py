"""Represents a Correlation Key."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class CorrelationKey(BaseElement):
    """A CorrelationKey is a composite key of CorrelationProperties that define extraction Expressions for Messages."""

    correlation_property_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "correlationPropertyRef",
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

    class Meta:
        name = "correlationKey"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
