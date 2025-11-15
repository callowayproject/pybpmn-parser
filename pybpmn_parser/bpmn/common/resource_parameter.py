"""Represents a Resource Parameter."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ResourceParameter(BaseElement):
    """A parameter for a resource used at runtime to define a query e.g., into an Organizational Directory."""

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
    is_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isRequired",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "resourceParameter"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
