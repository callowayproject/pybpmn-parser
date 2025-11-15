"""Definitions for the bpmn:documentation XML element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Documentation:
    """The Documentation element is used to annotate the BPMN element, such as descriptions and other documentation."""

    class Meta:
        name = "documentation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute is used to uniquely identify BPMN elements.
    The `id` is REQUIRED if this element is referenced or intended to be referenced by something else.
    If the element is not currently referenced and is never intended to be referenced, the `id` MAY be omitted."""

    text_format: str = field(
        default="text/plain",
        metadata={
            "name": "textFormat",
            "type": "Attribute",
        },
    )
    """This attribute identifies the format of the text. It MUST follow the mime-type format.
    The default is "text/plain."""

    content: str = field(
        metadata={
            "name": "#text",
            "type": "Wildcard",
            "mixed": True,
        },
    )
    """This attribute is used to capture the text descriptions of a BPMN element."""
