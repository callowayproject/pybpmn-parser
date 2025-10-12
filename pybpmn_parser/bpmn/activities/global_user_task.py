"""Represents a Global User Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.bpmn.types import NAMESPACES, ImplementationValue

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.activities.rendering import Rendering


@dataclass(kw_only=True)
class GlobalUserTask(GlobalTask):
    """A type of Global Task that represents a User Task."""

    rendering: list[Rendering] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    implementation: str | ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[GlobalUserTask]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.activities.rendering import Rendering

        if obj is None:
            return None

        baseclass = GlobalTask.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "implementation": obj.get("implementation", ImplementationValue.UNSPECIFIED),
                "rendering": [Rendering.parse(elem) for elem in obj.findall("./bpmn:rendering", NAMESPACES)],
            }
        )
        return cls(**attribs)
