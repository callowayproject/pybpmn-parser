"""Represents a Process."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.callable_element import CallableElement
from pybpmn_parser.bpmn.types import ProcessType
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    # from pybpmn_parser.bpmn.choreography.call_choreography import CallChoreography
    # from pybpmn_parser.bpmn.choreography.choreography_task import ChoreographyTask
    # from pybpmn_parser.bpmn.choreography.sub_choreography import SubChoreography
    from pybpmn_parser.bpmn.activities.business_rule_task import BusinessRuleTask
    from pybpmn_parser.bpmn.activities.call_activity import CallActivity
    from pybpmn_parser.bpmn.activities.manual_task import ManualTask
    from pybpmn_parser.bpmn.activities.receive_task import ReceiveTask
    from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
    from pybpmn_parser.bpmn.activities.script_task import ScriptTask
    from pybpmn_parser.bpmn.activities.send_task import SendTask
    from pybpmn_parser.bpmn.activities.service_task import ServiceTask
    from pybpmn_parser.bpmn.activities.sub_process import AdHocSubProcess, SubProcess, Transaction
    from pybpmn_parser.bpmn.activities.task import Task
    from pybpmn_parser.bpmn.activities.user_task import UserTask
    from pybpmn_parser.bpmn.common.artifact import Artifact
    from pybpmn_parser.bpmn.common.association import Association
    from pybpmn_parser.bpmn.common.correlation_subscription import CorrelationSubscription
    from pybpmn_parser.bpmn.common.flow_element import FlowElement
    from pybpmn_parser.bpmn.common.group import Group
    from pybpmn_parser.bpmn.common.sequence_flow import SequenceFlow
    from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
    from pybpmn_parser.bpmn.data.data_object import DataObject
    from pybpmn_parser.bpmn.data.data_object_reference import DataObjectReference
    from pybpmn_parser.bpmn.data.data_store_reference import DataStoreReference
    from pybpmn_parser.bpmn.data.property import Property
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
    from pybpmn_parser.bpmn.process.auditing import Auditing
    from pybpmn_parser.bpmn.process.lane import LaneSet
    from pybpmn_parser.bpmn.process.monitoring import Monitoring
    from pybpmn_parser.bpmn.process.performer import HumanPerformer, Performer, PotentialOwner


@register_element
@dataclass(kw_only=True)
class Process(CallableElement):
    """
    A Process describes a sequence or flow of Activities in an organization with the goal of carrying out work.
    """

    auditing: Optional[Auditing] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This attribute provides a hook for specifying audit-related properties."""

    monitoring: Optional[Monitoring] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This attribute provides a hook for specifying monitoring-related properties."""

    properties: list[Property] = field(
        default_factory=list,
        metadata={
            "name": "property",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Modeler-defined properties added to the Process.

    All Tasks and Sub-Processes SHALL have access to these properties."""

    lane_sets: list[LaneSet] = field(
        default_factory=list,
        metadata={
            "name": "laneSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """The LaneSets used in this Process."""

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
            "name": "transaction",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    tasks: list[Task] = field(
        default_factory=list,
        metadata={
            "name": "task",
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
    # sub_choreographies: list[SubChoreography] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "subChoreography",
    #         "type": "Element",
    #         "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    #     },
    # )
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
            "name": "event",
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
    # choreography_tasks: list[ChoreographyTask] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "choreographyTask",
    #         "type": "Element",
    #         "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    #     },
    # )
    # call_choreographies: list[CallChoreography] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "callChoreography",
    #         "type": "Element",
    #         "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    #     },
    # )
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
            "name": "group",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    associations: list[Association] = field(
        default_factory=list,
        metadata={
            "name": "association",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    artifacts: list[Artifact] = field(
        default_factory=list,
        metadata={
            "name": "artifact",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This attribute provides the list of Artifacts that are contained within the Process."""

    potential_owners: list[PotentialOwner] = field(
        default_factory=list,
        metadata={
            "name": "potentialOwner",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Potential owners of a User Task are persons who can claim and work on it."""

    human_performers: list[HumanPerformer] = field(
        default_factory=list,
        metadata={
            "name": "humanPerformer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    performers: list[Performer] = field(
        default_factory=list,
        metadata={
            "name": "performer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    resources: list[ResourceRole] = field(
        default_factory=list,
        metadata={
            "name": "resourceRole",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Defines the resource that will perform or will be responsible for the Activity.

    The resource, e.g., a performer, can be specified in the form of a specific individual, a group, an organization
    role or position, or an organization."""

    correlation_subscriptions: list[CorrelationSubscription] = field(
        default_factory=list,
        metadata={
            "name": "correlationSubscription",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Defines how to correlate incoming Messages against data in the Process context."""

    supports: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    """All executions of these Processes are valid for this Process."""

    process_type: ProcessType = field(
        default=ProcessType.NONE,
        metadata={
            "name": "processType",
            "type": "Attribute",
        },
    )
    """Provides additional information about the level of abstraction modeled by this Process."""

    is_closed: bool = field(
        default=False,
        metadata={
            "name": "isClosed",
            "type": "Attribute",
        },
    )
    """Can external interactions, e.g. sending/receiving external Messages, occur when the Process is executed."""

    is_executable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isExecutable",
            "type": "Attribute",
        },
    )
    """Is this process executable?."""

    definitional_collaboration_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "definitionalCollaborationRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    """The definitional Collaboration specifies the Participants the Process interacts with.

    More specifically, which individual service, Send or Receive Task, or Message Event, is connected to which
    Participant through Message Flows."""

    class Meta:
        name = "process"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
