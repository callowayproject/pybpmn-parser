"""Represents a Relationship."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.types import RelationshipDirection


@register_element
@dataclass(kw_only=True)
class Relationship(BaseElement):
    """A Relationship defines a relationship between two Elements."""

    class Meta:
        name = "relationship"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    source: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "is_reference": True,
        },
    )
    """This association defines artifacts that are augmented by the relationship."""

    target: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "is_reference": True,
        },
    )
    """This association defines artifacts used to extend the semantics of the source element(s)."""

    type_value: str = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    """The descriptive name of the element."""

    direction: Optional[RelationshipDirection] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute specifies the direction of the relationship."""
