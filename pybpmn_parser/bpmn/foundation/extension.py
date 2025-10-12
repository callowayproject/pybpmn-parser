"""Represents an Extension."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.foundation.documentation import Documentation


@dataclass(kw_only=True)
class Extension:
    """The Extension element binds/imports an ExtensionDefinition and its attributes to a BPMN model definition."""

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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Extension]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.foundation.documentation import Documentation

        if obj is None:
            return None

        return cls(
            documentation=[Documentation.parse(elem) for elem in obj.findall("./bpmn:documentation", NAMESPACES)],
            definition=obj.get("definition"),
            must_understand=strtobool(obj.get("mustUnderstand", "false")),
        )
