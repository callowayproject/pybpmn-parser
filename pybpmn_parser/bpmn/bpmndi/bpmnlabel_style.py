"""Model definition for BPMNLabelStyle."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.di.style import Style
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.dc.font import Font

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNLabelStyle(Style):
    """BPMNLabelStyle provides appearance options for a BPMNLabel."""

    class Meta:
        name = "BPMNLabelStyle"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    font: Font = field(
        metadata={
            "name": "Font",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/DD/20100524/DC",
            "required": True,
        }
    )
    """A font object that describes the properties of the font used for the labels that reference this style."""
