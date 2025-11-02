"""Represents a Global Business Rule Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class GlobalBusinessRuleTask(GlobalTask):
    """A type of Global Task that represents a Business Rule Task."""

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "globalBusinessRuleTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[GlobalBusinessRuleTask]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = GlobalTask.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.UNSPECIFIED),
            }
        )
        return cls(**attribs)
