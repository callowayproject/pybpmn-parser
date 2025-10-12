"""Represents the rendering of a User Task (Task UI)."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement


@dataclass(kw_only=True)
class Rendering(BaseElement):
    """The Rendering element provides an extensible mechanism for specifying UI renderings for User Tasks (Task UI)."""

    pass
