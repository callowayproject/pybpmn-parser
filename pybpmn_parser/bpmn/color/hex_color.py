"""Model definitions for the HexColor type."""

from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


@dataclass(kw_only=True)
class HexColor:
    """The `HexColor` type defines the color representation in this extension."""

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"#[0-9a-fA-F]{6}",
        },
    )
