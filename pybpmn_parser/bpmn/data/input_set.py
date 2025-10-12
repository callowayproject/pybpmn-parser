"""Represents a BPMN 2.0 input set."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class InputSet(BaseElement):
    """An InputSet is a collection of DataInput elements that define a valid set of inputs for an ioSpecification."""

    data_input_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "dataInputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """The DataInput elements that collectively make up this data requirement."""

    optional_input_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "optionalInputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """The DataInput elements that are part of the InputSet can be “unavailable” when the Activity starts executing.

    This association must reference a DataInput that is listed in `data_input_refs`."""

    while_executing_input_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "whileExecutingInputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """The DataInput elements that are a part of the InputSet can be evaluated while the Activity is executing.

    This association must reference a DataInput that is listed in the `dataInputRefs`."""

    output_set_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "outputSetRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """Specifies an Input/Output rule that defines which OutputSet is to be created when this InputSet is valid.

    This attribute is paired with the `inputSetRefs` attribute of OutputSets."""

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """A descriptive name for the input set."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[InputSet]:
        """Parse the given XML element."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "name": obj.get("name"),
                "data_input_refs": [elem.text for elem in obj.findall("./bpmn:dataInputRefs", NAMESPACES)],
                "optional_input_refs": [elem.text for elem in obj.findall("./bpmn:optionalInputRefs", NAMESPACES)],
                "while_executing_input_refs": [
                    elem.text for elem in obj.findall("./bpmn:whileExecutingInputRefs", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
