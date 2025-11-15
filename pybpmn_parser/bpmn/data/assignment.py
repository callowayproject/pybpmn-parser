"""Representation of an Assignment."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class Assignment(BaseElement):
    """Assignment is used to specify a simple mapping of data bpmn using a specified Expression language."""

    from_value: Expression = field(
        metadata={
            "name": "from",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    to: Expression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )

    class Meta:
        name = "assignment"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
