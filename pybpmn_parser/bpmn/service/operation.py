"""Represents an Operation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Operation(BaseElement):
    """An Operation defines Messages that are consumed and, optionally, produced when the Operation is called."""

    class Meta:
        name = "operation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    in_message_ref: str = field(
        metadata={
            "name": "inMessageRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
            "is_reference": True,
        }
    )
    """This attribute specifies the input Message of the Operation.

    An Operation has exactly one input Message."""

    out_message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "outMessageRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """This attribute specifies the output Message of the operation.

    An Operation has at most one input Message."""

    error_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "errorRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """This attribute specifies errors that the Operation may return.

    An Operation may refer to zero or more Error elements."""

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """The descriptive name of the element."""

    implementation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "implementationRef",
            "type": "Attribute",
        },
    )
