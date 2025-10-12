"""Represents a Script Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.task import Task
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ScriptTask(Task):
    """A Script Task is executed by a business process engine."""

    script: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    script_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "scriptFormat",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ScriptTask]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = Task.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        script = obj.find("./bpmn:script", NAMESPACES)
        attribs.update(
            {
                "script_format": obj.get("scriptFormat"),
                "script": script.text if script is not None else None,
            }
        )

        return cls(**attribs)
