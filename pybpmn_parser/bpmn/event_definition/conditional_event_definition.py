"""Represents a ConditionalEventDefinition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class ConditionalEventDefinition(EventDefinition):
    """Definition of a conditional event."""

    class Meta:
        name = "conditionalEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    condition: Expression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
