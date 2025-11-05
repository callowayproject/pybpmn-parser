"""Model definitions for border color."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


@register_element
@dataclass(kw_only=True)
class BorderColor:
    """The border color defines the contour line color of a `BPMNShape` and the line color of a `BPMNEdge`."""

    class Meta:
        name = "border-color"
        namespace = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"#[0-9a-fA-F]{6}",
        },
    )
