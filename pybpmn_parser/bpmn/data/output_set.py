"""Represents an Output Set."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class OutputSet(BaseElement):
    """An OutputSet is a collection of DataOutputs that can be produced as output from an Activity or Event."""

    data_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "dataOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    optional_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "optionalOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    while_executing_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "whileExecutingOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    input_set_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "inputSetRefs",
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
        name = "outputSet"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
