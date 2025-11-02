"""Represents the rendering of a User Task (Task UI)."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Rendering(BaseElement):
    """The Rendering element provides an extensible mechanism for specifying UI renderings for User Tasks (Task UI)."""

    class Meta:
        name = "rendering"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
