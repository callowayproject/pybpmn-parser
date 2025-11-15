"""Represents a Correlation Property."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.correlation_property_retrieval_expression import (
        CorrelationPropertyRetrievalExpression,
    )


@register_element
@dataclass(kw_only=True)
class CorrelationProperty(RootElement):
    """A CorrelationProperty is part of an associated CorrelationKey."""

    correlation_property_retrieval_expressions: list[CorrelationPropertyRetrievalExpression] = field(
        default_factory=list,
        metadata={
            "name": "correlationPropertyRetrievalExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
        },
    )
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

    class Meta:
        name = "correlationProperty"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
