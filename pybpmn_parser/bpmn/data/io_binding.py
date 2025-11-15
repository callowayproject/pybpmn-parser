"""Represents an input/output binding."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class IoBinding(BaseElement):
    """This binds an InputSet and an OutputSet to an operation defined in an interface."""

    operation_ref: str = field(
        metadata={
            "name": "operationRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    input_data_ref: str = field(
        metadata={
            "name": "inputDataRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    output_data_ref: str = field(
        metadata={
            "name": "outputDataRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    class Meta:
        name = "ioBinding"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
