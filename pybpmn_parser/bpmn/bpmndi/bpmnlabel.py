"""Model definitions for BPMN label."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.di.label import Label
from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNLabel(Label):
    """BPMNLabel is a label that depicts textual information about a BPMN element."""

    class Meta:
        name = "BPMNLabel"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    label_style: Optional[str] = field(
        default=None,
        metadata={
            "name": "labelStyle",
            "type": "Attribute",
        },
    )
    """An optional reference to a diagram's label style that gives the appearance options for the label."""
