"""Represents an input/output binding."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class IoBinding(BaseElement):
    """This binds an InputSet and an OutputSet to an operation defined in an interface."""

    operation_ref: str = field(
        metadata={
            "name": "operationRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    input_data_ref: str = field(
        metadata={
            "name": "inputDataRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    output_data_ref: str = field(
        metadata={
            "name": "outputDataRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[IoBinding]:
        """Parse an XML object into an IoBinding object."""
        if obj is None:
            return None

        attribs = asdict(BaseElement.parse(obj))
        attribs.update(
            {
                "operation_ref": obj.get("operationRef"),
                "input_data_ref": obj.get("inputDataRef"),
                "output_data_ref": obj.get("outputDataRef"),
            }
        )

        return cls(**attribs)
