"""Representation of a Text Annotation."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.artifact import Artifact
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class TextAnnotation(Artifact):
    """Text Annotations are a mechanism for a modeler to provide additional information for the reader of a Diagram."""

    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    text_format: str = field(
        default="text/plain",
        metadata={
            "name": "textFormat",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "textAnnotation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[TextAnnotation]:
        """Parse the given XML element into a TextAnnotation object."""
        if obj is None:
            return None

        baseclass = Artifact.parse(obj)
        attributes = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        text = obj.find("./bpmn:text", NAMESPACES)
        attributes.update(
            {
                "text": text.text if text is not None else None,
                "text_format": obj.get("textFormat", "text/plain"),
            }
        )

        return cls(**attributes)
