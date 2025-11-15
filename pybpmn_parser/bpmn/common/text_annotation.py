"""Representation of a Text Annotation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.common.artifact import Artifact
from pybpmn_parser.element_registry import register_element


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
