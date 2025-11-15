"""Represents a Data State."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class DataState(BaseElement):
    """The state of the data contained in the Data Object."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "dataState"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
