"""Represents an Error."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Error(RootElement):
    """An Error represents the content of an Error Event or the Fault of a failed Operation."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    error_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorCode",
            "type": "Attribute",
        },
    )
    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "error"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
