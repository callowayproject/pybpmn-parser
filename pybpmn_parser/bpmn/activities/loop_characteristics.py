"""Represents the loop characteristics of an activity."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import NAMESPACES, MultiInstanceFlowCondition
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.activities.complex_behavior_definition import ComplexBehaviorDefinition
    from pybpmn_parser.bpmn.common.expression import Expression
    from pybpmn_parser.bpmn.data.data_input import DataInput
    from pybpmn_parser.bpmn.data.data_output import DataOutput


@dataclass(kw_only=True)
class LoopCharacteristics(BaseElement):
    """
    The presence of LoopCharacteristics signifies that the Activity has looping behavior.

    LoopCharacteristics is an abstract class.
    """

    pass


@dataclass(kw_only=True)
class MultiInstanceLoopCharacteristics(LoopCharacteristics):
    """Allows for the creation of a desired number of Activity instances."""

    loop_cardinality: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "loopCardinality",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    loop_data_input_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "loopDataInputRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    loop_data_output_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "loopDataOutputRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    input_data_item: Optional[DataInput] = field(
        default=None,
        metadata={
            "name": "inputDataItem",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    output_data_item: Optional[DataOutput] = field(
        default=None,
        metadata={
            "name": "outputDataItem",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    complex_behavior_definition: list[ComplexBehaviorDefinition] = field(
        default_factory=list,
        metadata={
            "name": "complexBehaviorDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    completion_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "completionCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    is_sequential: bool = field(
        default=False,
        metadata={
            "name": "isSequential",
            "type": "Attribute",
        },
    )
    behavior: MultiInstanceFlowCondition = field(
        default=MultiInstanceFlowCondition.ALL,
        metadata={
            "type": "Attribute",
        },
    )
    one_behavior_event_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "oneBehaviorEventRef",
            "type": "Attribute",
        },
    )
    none_behavior_event_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "noneBehaviorEventRef",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[MultiInstanceLoopCharacteristics]:
        """Parse an XML element into a MultiInstanceLoopCharacteristics object."""
        from pybpmn_parser.bpmn.activities.complex_behavior_definition import ComplexBehaviorDefinition
        from pybpmn_parser.bpmn.common.expression import Expression
        from pybpmn_parser.bpmn.data.data_input import DataInput
        from pybpmn_parser.bpmn.data.data_output import DataOutput

        if obj is None:
            return None

        baseclass = LoopCharacteristics.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        loop_data_input_ref = obj.find("./bpmn:loopDataInputRef", NAMESPACES)
        loop_data_output_ref = obj.find("./bpmn:loopDataOutputRef", NAMESPACES)
        attribs.update(
            {
                "loop_cardinality": Expression.parse(obj.find("./bpmn:expression", NAMESPACES)),
                "loop_data_input_ref": loop_data_input_ref.text if loop_data_input_ref is not None else None,
                "loop_data_output_ref": loop_data_output_ref.text if loop_data_output_ref is not None else None,
                "input_data_item": DataInput.parse(obj.find("./bpmn:inputDataItem", NAMESPACES)),
                "output_data_item": DataOutput.parse(obj.find("./bpmn:outputDataItem", NAMESPACES)),
                "complex_behavior_definition": [
                    ComplexBehaviorDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:complexBehaviorDefinition", NAMESPACES)
                ],
                "completion_condition": Expression.parse(obj.find("./bpmn:completionCondition", NAMESPACES)),
                "is_sequential": strtobool(obj.get("isSequential", "false")),
                "behavior": obj.get("behavior", MultiInstanceFlowCondition.ALL),
                "one_behavior_event_ref": obj.get("oneBehaviorEventRef"),
                "none_behavior_event_ref": obj.get("noneBehaviorEventRef"),
            }
        )

        return cls(**attribs)


@dataclass(kw_only=True)
class StandardLoopCharacteristics(LoopCharacteristics):
    """The StandardLoopCharacteristics class defines looping behavior based on a boolean condition."""

    loop_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "loopCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    test_before: bool = field(
        default=False,
        metadata={
            "name": "testBefore",
            "type": "Attribute",
        },
    )
    loop_maximum: Optional[int] = field(
        default=None,
        metadata={
            "name": "loopMaximum",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[StandardLoopCharacteristics]:
        """Parse an XML element into a StandardLoopCharacteristics object."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = LoopCharacteristics.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}

        loop_maximum = obj.get("loopMaximum")
        attribs.update(
            {
                "loop_condition": Expression.parse(obj.find("./bpmn:expression", NAMESPACES)),
                "test_before": strtobool(obj.get("testBefore", "false")),
                "loop_maximum": int(loop_maximum) if loop_maximum is not None else None,
            }
        )

        return cls(**attribs)
