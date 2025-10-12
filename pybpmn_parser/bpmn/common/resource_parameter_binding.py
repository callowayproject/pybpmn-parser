"""The binding of a resource parameter to a formal expression."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import Expression, FormalExpression


@dataclass(kw_only=True)
class ResourceParameterBinding(BaseElement):
    """The binding of a resource parameter to a formal expression."""

    formal_expression: Optional[FormalExpression] = field(
        default=None,
        metadata={
            "name": "formalExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    expression: Optional[Expression] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ResourceParameterBinding]:
        """Parse an XML element into a ResourceParameterBinding object."""
        from pybpmn_parser.bpmn.common.expression import Expression, FormalExpression

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        attribs.update(
            {
                "formal_expression": FormalExpression.parse(obj.find("./bpmn:formalExpression", NAMESPACES)),
                "expression": Expression.parse(obj.find("./bpmn:expression", NAMESPACES)),
                "parameter_ref": obj.get("parameterRef", ""),
            }
        )

        return cls(**attribs)
