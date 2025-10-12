"""Definitions for the bpmn:documentation XML element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import lxml.etree as ET


@dataclass(kw_only=True)
class Documentation:
    """The Documentation element is used to annotate the BPMN element, such as descriptions and other documentation."""

    class Meta:
        name = "tDocumentation"

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
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )
    """This attribute is used to capture the text descriptions of a BPMN element."""

    @classmethod
    def parse(cls, obj: ET.Element) -> Documentation:
        """Parse an XML element into a Documentation object."""
        return cls(
            id=obj.get("id"),
            text_format=obj.get("textFormat", "text/plain"),
            content=obj.text,
        )
