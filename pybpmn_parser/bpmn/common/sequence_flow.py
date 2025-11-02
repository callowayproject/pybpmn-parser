"""Represents a Sequence Flow."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_element import FlowElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import strtobool
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class SequenceFlow(FlowElement):
    """The Sequence Flow element is used to define the sequence of execution between two FlowNodes."""

    condition_expression: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "conditionExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    source_ref: str = field(
        metadata={
            "name": "sourceRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    target_ref: str = field(
        metadata={
            "name": "targetRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    is_immediate: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isImmediate",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "sequenceFlow"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[SequenceFlow]:
        """Parse the given XML element."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = FlowElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        is_immediate = obj.get("isImmediate")
        attribs.update(
            {
                "condition_expression": Expression.parse(obj.find("./bpmn:conditionExpression", NAMESPACES)),
                "source_ref": obj.get("sourceRef"),
                "target_ref": obj.get("targetRef"),
                "is_immediate": strtobool(is_immediate) if is_immediate is not None else None,
            }
        )

        return cls(**attribs)
