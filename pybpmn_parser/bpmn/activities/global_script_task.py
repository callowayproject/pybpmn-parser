"""Represents a Global Script Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.process.global_task import GlobalTask

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class GlobalScriptTask(GlobalTask):
    """A type of Global Task that represents a Script Task."""

    script: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    script_language: Optional[str] = field(
        default=None,
        metadata={
            "name": "scriptLanguage",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[GlobalScriptTask]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None
        baseclass = GlobalTask.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "script": obj.findtext("./bpmn:script"),
                "script_language": obj.get("scriptLanguage"),
            }
        )
        return cls(**attribs)
