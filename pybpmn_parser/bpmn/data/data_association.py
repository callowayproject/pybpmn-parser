"""Represents a Data Association."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import FormalExpression
    from pybpmn_parser.bpmn.data.assignment import Assignment


@dataclass(kw_only=True)
class DataAssociation(BaseElement):
    """
    Data Associations move data between Data Objects/Properties, and inputs/outputs of Activities/Processes/etc.
    """

    source_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "sourceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
            "is_reference": True,
        }
    )
    transformation: Optional[FormalExpression] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    assignments: list[Assignment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[DataAssociation]:
        """Parse an XML element into a DataAssociation object."""
        from pybpmn_parser.bpmn.common.expression import FormalExpression
        from pybpmn_parser.bpmn.data.assignment import Assignment

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        attribs.update(
            {
                "source_ref": [elem.text for elem in obj.findall("./bpmn:sourceRef", NAMESPACES)],
                "target_ref": obj.find("./bpmn:targetRef", NAMESPACES).text,
                "transformation": FormalExpression.parse(obj.find("./bpmn:transformation", NAMESPACES)),
                "assignments": [Assignment.parse(elem) for elem in obj.findall("./bpmn:assignment", NAMESPACES)],
            }
        )

        return cls(**attribs)


@dataclass(kw_only=True)
class DataOutputAssociation(DataAssociation):
    """DataOutputAssociation is used to model how data is pulled from item-aware bpmn."""

    pass


@dataclass(kw_only=True)
class DataInputAssociation(DataAssociation):
    """DataInputAssociation is used to model how data is pushed into item-aware bpmn."""

    pass
