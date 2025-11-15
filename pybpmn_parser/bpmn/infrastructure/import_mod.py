"""Represents an Import."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.element_registry import register_element


@register_element
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

    class Meta:
        name = "import"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
