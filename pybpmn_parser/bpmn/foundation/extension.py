"""Represents an Extension."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.foundation.documentation import Documentation


@register_element
@dataclass(kw_only=True)
class Extension:
    """The Extension element binds/imports an ExtensionDefinition and its attributes to a BPMN model definition."""

    class Meta:
        name = "extension"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    documentation: list[Documentation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This attribute is used to annotate the BPMN element, such as descriptions and other documentation."""

    definition: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """Defines the content of the extension.

    Note that in the XML schema, this definition is provided by an external XML schema file and is simply
    referenced by QName."""

    must_understand: bool = field(
        default=False,
        metadata={
            "name": "mustUnderstand",
            "type": "Attribute",
        },
    )
    """This flag defines if the semantics defined by the extension definition and its attribute definition MUST
    be understood by the BPMN adopter in order to process the BPMN model correctly. Defaults to False."""
