"""Represents an Output Set."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class OutputSet(BaseElement):
    """An OutputSet is a collection of DataOutputs that can be produced as output from an Activity or Event."""

    data_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "dataOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    optional_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "optionalOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    while_executing_output_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "whileExecutingOutputRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    input_set_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "inputSetRefs",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "outputSet"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[OutputSet]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "data_output_refs": [elem.text for elem in obj.findall("./bpmn:dataOutputRefs", NAMESPACES)],
                "name": obj.get("name"),
                "input_set_refs": [elem.text for elem in obj.findall("./bpmn:inputSetRefs", NAMESPACES)],
                "optional_output_refs": [elem.text for elem in obj.findall("./bpmn:optionalOutputRefs", NAMESPACES)],
                "while_executing_output_refs": [
                    elem.text for elem in obj.findall("./bpmn:whileExecutingOutputRefs", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
