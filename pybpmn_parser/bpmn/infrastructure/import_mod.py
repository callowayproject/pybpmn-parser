"""Represents an Import."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class Import:
    """This class references external BPMN or non-BPMN bpmn."""

    namespace: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    location: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    import_type: str = field(
        metadata={
            "name": "importType",
            "type": "Attribute",
            "required": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Import]:
        """Parse an XML object into an Import object."""
        if obj is None:
            return None

        return cls(
            namespace=obj.get("namespace", ""),
            location=obj.get("location", ""),
            import_type=obj.get("importType", ""),
        )
