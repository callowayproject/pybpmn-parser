"""Represents a SubProcess element in BPMN 2.0."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.activities.activity import Activity
from pybpmn_parser.bpmn.types import NAMESPACES, AdHocOrdering, TransactionMethodValue
from pybpmn_parser.core import strtobool

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.activities.business_rule_task import BusinessRuleTask
    from pybpmn_parser.bpmn.activities.call_activity import CallActivity
    from pybpmn_parser.bpmn.activities.manual_task import ManualTask
    from pybpmn_parser.bpmn.activities.receive_task import ReceiveTask
    from pybpmn_parser.bpmn.activities.script_task import ScriptTask
    from pybpmn_parser.bpmn.activities.send_task import SendTask
    from pybpmn_parser.bpmn.activities.service_task import ServiceTask
    from pybpmn_parser.bpmn.activities.task import Task
    from pybpmn_parser.bpmn.activities.user_task import UserTask
    from pybpmn_parser.bpmn.choreography.call_choreography import CallChoreography
    from pybpmn_parser.bpmn.choreography.choreography_task import ChoreographyTask
    from pybpmn_parser.bpmn.choreography.sub_choreography import SubChoreography
    from pybpmn_parser.bpmn.common.artifact import Artifact
    from pybpmn_parser.bpmn.common.association import Association
    from pybpmn_parser.bpmn.common.expression import Expression
    from pybpmn_parser.bpmn.common.flow_element import FlowElement
    from pybpmn_parser.bpmn.common.group import Group
    from pybpmn_parser.bpmn.common.sequence_flow import SequenceFlow
    from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
    from pybpmn_parser.bpmn.data.data_object import DataObject
    from pybpmn_parser.bpmn.data.data_object_reference import DataObjectReference
    from pybpmn_parser.bpmn.data.data_store_reference import DataStoreReference
    from pybpmn_parser.bpmn.event import Event
    from pybpmn_parser.bpmn.event.boundary_event import BoundaryEvent
    from pybpmn_parser.bpmn.event.end_event import EndEvent
    from pybpmn_parser.bpmn.event.implicit_throw_event import ImplicitThrowEvent
    from pybpmn_parser.bpmn.event.intermediate_catch_event import IntermediateCatchEvent
    from pybpmn_parser.bpmn.event.intermediate_throw_event import IntermediateThrowEvent
    from pybpmn_parser.bpmn.event.start_event import StartEvent
    from pybpmn_parser.bpmn.gateway.complex_gateway import ComplexGateway
    from pybpmn_parser.bpmn.gateway.event_based_gateway import EventBasedGateway
    from pybpmn_parser.bpmn.gateway.exclusive_gateway import ExclusiveGateway
    from pybpmn_parser.bpmn.gateway.inclusive_gateway import InclusiveGateway
    from pybpmn_parser.bpmn.gateway.parallel_gateway import ParallelGateway
    from pybpmn_parser.bpmn.process.lane import LaneSet


@dataclass(kw_only=True)
class SubProcess(Activity):
    """A SubProcess is a compound activity that represents a collection of other tasks and SubProcesses."""

    lane_sets: list[LaneSet] = field(
        default_factory=list,
        metadata={
            "name": "laneSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    user_tasks: list[UserTask] = field(
        default_factory=list,
        metadata={
            "name": "userTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    transactions: list[Transaction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    tasks: list[Task] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    sub_processes: list[SubProcess] = field(
        default_factory=list,
        metadata={
            "name": "subProcess",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    sub_choreographies: list[SubChoreography] = field(
        default_factory=list,
        metadata={
            "name": "subChoreography",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    start_events: list[StartEvent] = field(
        default_factory=list,
        metadata={
            "name": "startEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    service_tasks: list[ServiceTask] = field(
        default_factory=list,
        metadata={
            "name": "serviceTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    sequence_flows: list[SequenceFlow] = field(
        default_factory=list,
        metadata={
            "name": "sequenceFlow",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    send_tasks: list[SendTask] = field(
        default_factory=list,
        metadata={
            "name": "sendTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    script_tasks: list[ScriptTask] = field(
        default_factory=list,
        metadata={
            "name": "scriptTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    receive_tasks: list[ReceiveTask] = field(
        default_factory=list,
        metadata={
            "name": "receiveTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    parallel_gateways: list[ParallelGateway] = field(
        default_factory=list,
        metadata={
            "name": "parallelGateway",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    manual_tasks: list[ManualTask] = field(
        default_factory=list,
        metadata={
            "name": "manualTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    intermediate_throw_events: list[IntermediateThrowEvent] = field(
        default_factory=list,
        metadata={
            "name": "intermediateThrowEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    intermediate_catch_events: list[IntermediateCatchEvent] = field(
        default_factory=list,
        metadata={
            "name": "intermediateCatchEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    inclusive_gateways: list[InclusiveGateway] = field(
        default_factory=list,
        metadata={
            "name": "inclusiveGateway",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    implicit_throw_events: list[ImplicitThrowEvent] = field(
        default_factory=list,
        metadata={
            "name": "implicitThrowEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    exclusive_gateways: list[ExclusiveGateway] = field(
        default_factory=list,
        metadata={
            "name": "exclusiveGateway",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_based_gateways: list[EventBasedGateway] = field(
        default_factory=list,
        metadata={
            "name": "eventBasedGateway",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    events: list[Event] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    end_events: list[EndEvent] = field(
        default_factory=list,
        metadata={
            "name": "endEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    data_store_references: list[DataStoreReference] = field(
        default_factory=list,
        metadata={
            "name": "dataStoreReference",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    data_object_references: list[DataObjectReference] = field(
        default_factory=list,
        metadata={
            "name": "dataObjectReference",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    data_objects: list[DataObject] = field(
        default_factory=list,
        metadata={
            "name": "dataObject",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    complex_gateways: list[ComplexGateway] = field(
        default_factory=list,
        metadata={
            "name": "complexGateway",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    choreography_tasks: list[ChoreographyTask] = field(
        default_factory=list,
        metadata={
            "name": "choreographyTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    call_choreographies: list[CallChoreography] = field(
        default_factory=list,
        metadata={
            "name": "callChoreography",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    call_activities: list[CallActivity] = field(
        default_factory=list,
        metadata={
            "name": "callActivity",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    business_rule_tasks: list[BusinessRuleTask] = field(
        default_factory=list,
        metadata={
            "name": "businessRuleTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    boundary_events: list[BoundaryEvent] = field(
        default_factory=list,
        metadata={
            "name": "boundaryEvent",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    ad_hoc_sub_processes: list[AdHocSubProcess] = field(
        default_factory=list,
        metadata={
            "name": "adHocSubProcess",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    flow_elements: list[FlowElement] = field(
        default_factory=list,
        metadata={
            "name": "flowElement",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    text_annotations: list[TextAnnotation] = field(
        default_factory=list,
        metadata={
            "name": "textAnnotation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    groups: list[Group] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    associations: list[Association] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    artifacts: list[Artifact] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    triggered_by_event: bool = field(
        default=False,
        metadata={
            "name": "triggeredByEvent",
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[SubProcess]:
        """Parse an XML object into a SubProcess object."""
        from pybpmn_parser.bpmn.activities.business_rule_task import BusinessRuleTask
        from pybpmn_parser.bpmn.activities.call_activity import CallActivity
        from pybpmn_parser.bpmn.activities.manual_task import ManualTask
        from pybpmn_parser.bpmn.activities.receive_task import ReceiveTask
        from pybpmn_parser.bpmn.activities.script_task import ScriptTask
        from pybpmn_parser.bpmn.activities.send_task import SendTask
        from pybpmn_parser.bpmn.activities.service_task import ServiceTask
        from pybpmn_parser.bpmn.activities.task import Task
        from pybpmn_parser.bpmn.activities.user_task import UserTask
        from pybpmn_parser.bpmn.choreography.call_choreography import CallChoreography
        from pybpmn_parser.bpmn.choreography.choreography_task import ChoreographyTask
        from pybpmn_parser.bpmn.choreography.sub_choreography import SubChoreography
        from pybpmn_parser.bpmn.common.artifact import Artifact
        from pybpmn_parser.bpmn.common.association import Association
        from pybpmn_parser.bpmn.common.flow_element import FlowElement
        from pybpmn_parser.bpmn.common.group import Group
        from pybpmn_parser.bpmn.common.sequence_flow import SequenceFlow
        from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
        from pybpmn_parser.bpmn.data.data_object import DataObject
        from pybpmn_parser.bpmn.data.data_object_reference import DataObjectReference
        from pybpmn_parser.bpmn.data.data_store_reference import DataStoreReference
        from pybpmn_parser.bpmn.event import Event
        from pybpmn_parser.bpmn.event.boundary_event import BoundaryEvent
        from pybpmn_parser.bpmn.event.end_event import EndEvent
        from pybpmn_parser.bpmn.event.implicit_throw_event import ImplicitThrowEvent
        from pybpmn_parser.bpmn.event.intermediate_catch_event import IntermediateCatchEvent
        from pybpmn_parser.bpmn.event.intermediate_throw_event import IntermediateThrowEvent
        from pybpmn_parser.bpmn.event.start_event import StartEvent
        from pybpmn_parser.bpmn.gateway.complex_gateway import ComplexGateway
        from pybpmn_parser.bpmn.gateway.event_based_gateway import EventBasedGateway
        from pybpmn_parser.bpmn.gateway.exclusive_gateway import ExclusiveGateway
        from pybpmn_parser.bpmn.gateway.inclusive_gateway import InclusiveGateway
        from pybpmn_parser.bpmn.gateway.parallel_gateway import ParallelGateway
        from pybpmn_parser.bpmn.process.lane import LaneSet

        if obj is None:
            return None

        baseclass = Activity.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "ad_hoc_sub_processes": [
                    AdHocSubProcess.parse(elem) for elem in obj.findall("./bpmn:adHocSubProcess", NAMESPACES)
                ],
                "artifacts": [Artifact.parse(elem) for elem in obj.findall("./bpmn:artifact", NAMESPACES)],
                "associations": [Association.parse(elem) for elem in obj.findall("./bpmn:association", NAMESPACES)],
                "boundary_events": [
                    BoundaryEvent.parse(elem) for elem in obj.findall("./bpmn:boundaryEvent", NAMESPACES)
                ],
                "business_rule_tasks": [
                    BusinessRuleTask.parse(elem) for elem in obj.findall("./bpmn:businessRuleTask", NAMESPACES)
                ],
                "call_activities": [
                    CallActivity.parse(elem) for elem in obj.findall("./bpmn:callActivity", NAMESPACES)
                ],
                "call_choreographies": [
                    CallChoreography.parse(elem) for elem in obj.findall("./bpmn:callChoreography", NAMESPACES)
                ],
                "choreography_tasks": [
                    ChoreographyTask.parse(elem) for elem in obj.findall("./bpmn:choreographyTask", NAMESPACES)
                ],
                "complex_gateways": [
                    ComplexGateway.parse(elem) for elem in obj.findall("./bpmn:complexGateway", NAMESPACES)
                ],
                "data_objects": [DataObject.parse(elem) for elem in obj.findall("./bpmn:dataObject", NAMESPACES)],
                "data_object_references": [
                    DataObjectReference.parse(elem) for elem in obj.findall("./bpmn:dataObjectReference", NAMESPACES)
                ],
                "data_store_references": [
                    DataStoreReference.parse(elem) for elem in obj.findall("./bpmn:dataStoreReference", NAMESPACES)
                ],
                "end_events": [EndEvent.parse(elem) for elem in obj.findall("./bpmn:endEvent", NAMESPACES)],
                "events": [Event.parse(elem) for elem in obj.findall("./bpmn:event", NAMESPACES)],
                "event_based_gateways": [
                    EventBasedGateway.parse(elem) for elem in obj.findall("./bpmn:eventBasedGateway", NAMESPACES)
                ],
                "exclusive_gateways": [
                    ExclusiveGateway.parse(elem) for elem in obj.findall("./bpmn:exclusiveGateway", NAMESPACES)
                ],
                "flow_elements": [FlowElement.parse(elem) for elem in obj.findall("./bpmn:flowElement", NAMESPACES)],
                "groups": [Group.parse(elem) for elem in obj.findall("./bpmn:group", NAMESPACES)],
                "implicit_throw_events": [
                    ImplicitThrowEvent.parse(elem) for elem in obj.findall("./bpmn:implicitThrowEvent", NAMESPACES)
                ],
                "inclusive_gateways": [
                    InclusiveGateway.parse(elem) for elem in obj.findall("./bpmn:inclusiveGateway", NAMESPACES)
                ],
                "intermediate_catch_events": [
                    IntermediateCatchEvent.parse(elem)
                    for elem in obj.findall("./bpmn:intermediateCatchEvent", NAMESPACES)
                ],
                "intermediate_throw_events": [
                    IntermediateThrowEvent.parse(elem)
                    for elem in obj.findall("./bpmn:intermediateThrowEvent", NAMESPACES)
                ],
                "lane_sets": [LaneSet.parse(elem) for elem in obj.findall("./bpmn:laneSet", NAMESPACES)],
                "manual_tasks": [ManualTask.parse(elem) for elem in obj.findall("./bpmn:manualTask", NAMESPACES)],
                "parallel_gateways": [
                    ParallelGateway.parse(elem) for elem in obj.findall("./bpmn:parallelGateway", NAMESPACES)
                ],
                "receive_tasks": [ReceiveTask.parse(elem) for elem in obj.findall("./bpmn:receiveTask", NAMESPACES)],
                "script_tasks": [ScriptTask.parse(elem) for elem in obj.findall("./bpmn:scriptTask", NAMESPACES)],
                "send_tasks": [SendTask.parse(elem) for elem in obj.findall("./bpmn:sendTask", NAMESPACES)],
                "sequence_flows": [
                    SequenceFlow.parse(elem) for elem in obj.findall("./bpmn:sequenceFlow", NAMESPACES)
                ],
                "service_tasks": [ServiceTask.parse(elem) for elem in obj.findall("./bpmn:serviceTask", NAMESPACES)],
                "start_events": [StartEvent.parse(elem) for elem in obj.findall("./bpmn:startEvent", NAMESPACES)],
                "sub_choreographies": [
                    SubChoreography.parse(elem) for elem in obj.findall("./bpmn:subChoreography", NAMESPACES)
                ],
                "sub_processes": [SubProcess.parse(elem) for elem in obj.findall("./bpmn:subProcess", NAMESPACES)],
                "tasks": [Task.parse(elem) for elem in obj.findall("./bpmn:task", NAMESPACES)],
                "text_annotations": [
                    TextAnnotation.parse(elem) for elem in obj.findall("./bpmn:textAnnotation", NAMESPACES)
                ],
                "transactions": [Transaction.parse(elem) for elem in obj.findall("./bpmn:transaction", NAMESPACES)],
                "user_tasks": [UserTask.parse(elem) for elem in obj.findall("./bpmn:userTask", NAMESPACES)],
            }
        )

        return cls(**attribs)


@dataclass(kw_only=True)
class AdHocSubProcess(SubProcess):
    """An AdHocSubProcess is a special kind of SubProcess."""

    completion_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "completionCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    cancel_remaining_instances: bool = field(
        default=True,
        metadata={
            "name": "cancelRemainingInstances",
            "type": "Attribute",
        },
    )
    ordering: Optional[AdHocOrdering] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[AdHocSubProcess]:
        """Parse an XML object into an AdHocSubProcess object."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = SubProcess.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "completion_condition": Expression.parse(obj.find("./bpmn:completionCondition", NAMESPACES)),
                "cancel_remaining_instances": strtobool(obj.get("cancelRemainingInstances", "true")),
                "ordering": obj.get("ordering"),
            }
        )
        return cls(**attribs)


@dataclass(kw_only=True)
class Transaction(SubProcess):
    """A Transaction has a special behavior that is controlled through a transaction protocol."""

    method: str | TransactionMethodValue = field(
        default=TransactionMethodValue.COMPENSATE,
        metadata={
            "type": "Attribute",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Transaction]:
        """Parse an XML object into a Transaction object."""
        if obj is None:
            return None

        baseclass = SubProcess.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "method": obj.get("method", TransactionMethodValue.COMPENSATE),
            }
        )
        return cls(**attribs)
