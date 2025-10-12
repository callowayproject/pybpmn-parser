"""Represents an Expression."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class Expression(BaseElement):  # Is Abstract
    """The Expression class is used to specify an Expression using natural-language text."""

    pass


@dataclass(kw_only=True)
class FormalExpression(Expression):
    """The FormalExpression class is used to specify an executable Expression using a specified Expression language."""

    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    evaluates_to_type_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "evaluatesToTypeRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[FormalExpression]:
        """Parse a XML object into a FormalExpression object."""
        if obj is None:
            return None

        baseclass = Expression.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "language": obj.get("language"),
                "evaluates_to_type_ref": obj.get("evaluatesToTypeRef"),
            }
        )

        return cls(**attribs)
