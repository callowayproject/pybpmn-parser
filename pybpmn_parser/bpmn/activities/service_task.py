"""Represents a Service Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET


@register_element
@dataclass(kw_only=True)
class ServiceTask(Task):
    """
    A Service Task is a Task that uses some sort of service, which could be a Web service or an automated application.
    """

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.WEB_SERVICE,
        metadata={
            "type": "Attribute",
        },
    )
    operation_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "serviceTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ServiceTask]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = Task.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.WEB_SERVICE),
                "operation_ref": obj.get("operationRef"),
            }
        )
        return cls(**attribs)
