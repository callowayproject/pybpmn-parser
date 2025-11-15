"""Represents a BPMN Flow Element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.process.auditing import Auditing
    from pybpmn_parser.bpmn.process.monitoring import Monitoring


@register_element
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

    class Meta:
        name = "flowElement"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
