"""Model definition of a Font."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.element_registry import register_element

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DC"


@register_element
@dataclass(kw_only=True)
class Font:
    """Font specifies the characteristics of a given font through a set of font properties."""

    class Meta:
        name = "Font"
        namespace = "http://www.omg.org/spec/DD/20100524/DC"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The name of the font (e.g., "Times New Roman," "Arial," and "Helvetica")."""

    size: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """A non-negative real number representing the size of the font (expressed in the used unit of length)."""

    is_bold: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isBold",
            "type": "Attribute",
        },
    )
    """Whether the font has a **bold** style."""

    is_italic: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isItalic",
            "type": "Attribute",
        },
    )
    """Whether the font has an _italic_ style."""

    is_underline: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isUnderline",
            "type": "Attribute",
        },
    )
    """Whether the font has an underline style."""

    is_strike_through: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isStrikeThrough",
            "type": "Attribute",
        },
    )
    """Whether the font has a ~~strike-through~~ style."""
