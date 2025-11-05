"""Model definitions for BPMN Color."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


@register_element
@dataclass(kw_only=True)
class Color:
    """The color attribute specifies the text color of a `BPMNLabel`."""

    class Meta:
        name = "color"
        namespace = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"#[0-9a-fA-F]{6}",
        },
    )
