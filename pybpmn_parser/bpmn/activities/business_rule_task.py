"""Represents a Business Rule Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import ImplementationValue

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class BusinessRuleTask(Task):
    """
    A Business Rule Task is a Task that uses a Business Rule to determine whether to proceed with the workflow.

    A Business Rule Task provides a mechanism for the Process to provide input to a Business Rules Engine and to get
    the output of calculations that the Business Rules Engine might provide.
    """

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute specifies the technology to be used for implementing the Business Rule Task.

    Valid values are "##unspecified" for leaving the implementation technology open,
    "##WebService" for the Web service technology, or a URI identifying any other technology or coordination protocol.
    The default technology for this task is unspecified."""

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[BusinessRuleTask]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = Task.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.UNSPECIFIED),
            }
        )
        return cls(**attribs)
