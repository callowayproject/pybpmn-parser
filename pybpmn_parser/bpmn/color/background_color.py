"""Model of BackgroundColor."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


@register_element
@dataclass(kw_only=True)
class BackgroundColor:
    """The background color defines the fill color of a `BPMNShape`."""

    class Meta:
        name = "background-color"
        namespace = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"#[0-9a-fA-F]{6}",
        },
    )
