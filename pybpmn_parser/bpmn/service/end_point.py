"""Represents an EndPoint."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class EndPoint(RootElement):
    """The EndPoint element may be extended with endpoint reference definitions introduced in other specifications."""

    class Meta:
        name = "endPoint"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
