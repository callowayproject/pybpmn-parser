"""Represents a Correlation Property Retrieval Expression."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import FormalExpression


@dataclass(kw_only=True)
class CorrelationPropertyRetrievalExpression(BaseElement):
    """A CorrelationPropertyRetrievalExpression specifies how to extract CorrelationProperties of a Message."""

    message_path: FormalExpression = field(
        metadata={
            "name": "messagePath",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    message_ref: str = field(
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[CorrelationPropertyRetrievalExpression]:
        """Parse XML into this class."""
        from pybpmn_parser.bpmn.common.expression import FormalExpression

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "message_ref": obj.get("messageRef"),
                "message_path": FormalExpression.parse(obj.find("./bpmn:messagePath", NAMESPACES)),
            }
        )
        return cls(**attribs)
