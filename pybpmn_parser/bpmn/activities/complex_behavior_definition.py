"""Represents a Complex Behavior Definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    import lxml.etree as ET

    from pybpmn_parser.bpmn.common.expression import FormalExpression
    from pybpmn_parser.bpmn.event.implicit_throw_event import ImplicitThrowEvent


@register_element
@dataclass(kw_only=True)
class ComplexBehaviorDefinition(BaseElement):
    """
    This controls when and which Events are thrown if the behavior of the Multi-Instance Activity is set to complex.
    """

    condition: FormalExpression = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "required": True,
        }
    )
    event: Optional[ImplicitThrowEvent] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    class Meta:
        name = "complexBehaviorDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ComplexBehaviorDefinition]:
        """Parse an XML element into a ComplexBehaviorDefinition object."""
        from pybpmn_parser.bpmn.common.expression import FormalExpression
        from pybpmn_parser.bpmn.event.implicit_throw_event import ImplicitThrowEvent

        if obj is None:
            return None

        baseclass = BaseElement.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "condition": FormalExpression.parse(obj.find("./bpmn:condition", NAMESPACES)),
                "event": ImplicitThrowEvent.parse(obj.find("./bpmn:event", NAMESPACES)),
            }
        )

        return cls(**attribs)
