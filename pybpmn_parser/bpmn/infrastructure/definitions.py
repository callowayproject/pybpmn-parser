"""Represents the BPMN definitions object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import xmltodict
from lxml import etree as ET

from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    # from pybpmn_parser.bpmn.choreography.choreography import Choreography
    # from pybpmn_parser.bpmn.choreography.global_choreography_task import GlobalChoreographyTask

    from pybpmn_parser.bpmn.activities.global_business_rule_task import GlobalBusinessRuleTask
    from pybpmn_parser.bpmn.activities.global_manual_task import GlobalManualTask
    from pybpmn_parser.bpmn.activities.global_script_task import GlobalScriptTask
    from pybpmn_parser.bpmn.activities.global_user_task import GlobalUserTask
    from pybpmn_parser.bpmn.collaboration.collaboration import Collaboration
    from pybpmn_parser.bpmn.collaboration.participant import PartnerEntity, PartnerRole
    from pybpmn_parser.bpmn.common.category import Category
    from pybpmn_parser.bpmn.common.correlation_property import CorrelationProperty
    from pybpmn_parser.bpmn.common.error import Error
    from pybpmn_parser.bpmn.common.item_definition import ItemDefinition
    from pybpmn_parser.bpmn.common.message import Message
    from pybpmn_parser.bpmn.common.resource import Resource
    from pybpmn_parser.bpmn.conversation.global_conversation import GlobalConversation
    from pybpmn_parser.bpmn.data.data_store import DataStore
    from pybpmn_parser.bpmn.event.escalation import Escalation
    from pybpmn_parser.bpmn.event.signal import Signal
    from pybpmn_parser.bpmn.event_definition.cancel_event_definition import CancelEventDefinition
    from pybpmn_parser.bpmn.event_definition.compensate_event_definition import CompensateEventDefinition
    from pybpmn_parser.bpmn.event_definition.conditional_event_definition import ConditionalEventDefinition
    from pybpmn_parser.bpmn.event_definition.error_event_definition import ErrorEventDefinition
    from pybpmn_parser.bpmn.event_definition.escalation_event_definition import EscalationEventDefinition
    from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
    from pybpmn_parser.bpmn.event_definition.link_event_definition import LinkEventDefinition
    from pybpmn_parser.bpmn.event_definition.message_event_definition import MessageEventDefinition
    from pybpmn_parser.bpmn.event_definition.signal_event_definition import SignalEventDefinition
    from pybpmn_parser.bpmn.event_definition.terminate_event_definition import TerminateEventDefinition
    from pybpmn_parser.bpmn.event_definition.timer_event_definition import TimerEventDefinition
    from pybpmn_parser.bpmn.foundation.base_element import RootElement
    from pybpmn_parser.bpmn.foundation.extension import Extension
    from pybpmn_parser.bpmn.foundation.relationship import Relationship
    from pybpmn_parser.bpmn.infrastructure.import_mod import Import
    from pybpmn_parser.bpmn.process.global_task import GlobalTask
    from pybpmn_parser.bpmn.process.process import Process
    from pybpmn_parser.bpmn.service.end_point import EndPoint
    from pybpmn_parser.bpmn.service.interface import Interface


@register_element
@dataclass(kw_only=True)
class Definitions:
    """
    The Definitions class is the outermost object container for all BPMN elements.

    It defines the scope of visibility and the namespace for all contained elements.
    The interchange of BPMN files will always be through one or more Definitions.
    """

    imports: list[Import] = field(
        default_factory=list,
        metadata={
            "name": "import",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    extensions: list[Extension] = field(
        default_factory=list,
        metadata={
            "name": "extension",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    signals: list[Signal] = field(
        default_factory=list,
        metadata={
            "name": "signal",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    resources: list[Resource] = field(
        default_factory=list,
        metadata={
            "name": "resource",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    processes: list[Process] = field(
        default_factory=list,
        metadata={
            "name": "process",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    partner_roles: list[PartnerRole] = field(
        default_factory=list,
        metadata={
            "name": "partnerRole",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    partner_entities: list[PartnerEntity] = field(
        default_factory=list,
        metadata={
            "name": "partnerEntity",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    messages: list[Message] = field(
        default_factory=list,
        metadata={
            "name": "message",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    item_definitions: list[ItemDefinition] = field(
        default_factory=list,
        metadata={
            "name": "itemDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    interfaces: list[Interface] = field(
        default_factory=list,
        metadata={
            "name": "interface",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_user_tasks: list[GlobalUserTask] = field(
        default_factory=list,
        metadata={
            "name": "globalUserTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_tasks: list[GlobalTask] = field(
        default_factory=list,
        metadata={
            "name": "globalTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_script_tasks: list[GlobalScriptTask] = field(
        default_factory=list,
        metadata={
            "name": "globalScriptTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_manual_tasks: list[GlobalManualTask] = field(
        default_factory=list,
        metadata={
            "name": "globalManualTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_business_rule_tasks: list[GlobalBusinessRuleTask] = field(
        default_factory=list,
        metadata={
            "name": "globalBusinessRuleTask",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    timer_event_definitions: list[TimerEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "timerEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    terminate_event_definitions: list[TerminateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "terminateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    signal_event_definitions: list[SignalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "signalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    message_event_definitions: list[MessageEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "messageEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    link_event_definitions: list[LinkEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "linkEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    escalation_event_definitions: list[EscalationEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "escalationEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    error_event_definitions: list[ErrorEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "errorEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    conditional_event_definitions: list[ConditionalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "conditionalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    compensate_event_definitions: list[CompensateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "compensateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    cancel_event_definitions: list[CancelEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "cancelEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_definitions: list[EventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "eventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    escalations: list[Escalation] = field(
        default_factory=list,
        metadata={
            "name": "escalation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    errors: list[Error] = field(
        default_factory=list,
        metadata={
            "name": "error",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    end_points: list[EndPoint] = field(
        default_factory=list,
        metadata={
            "name": "endPoint",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    data_stores: list[DataStore] = field(
        default_factory=list,
        metadata={
            "name": "dataStore",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    correlation_properties: list[CorrelationProperty] = field(
        default_factory=list,
        metadata={
            "name": "correlationProperty",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    global_conversations: list[GlobalConversation] = field(
        default_factory=list,
        metadata={
            "name": "globalConversation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    # global_choreography_tasks: list[GlobalChoreographyTask] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "globalChoreographyTask",
    #         "type": "Element",
    #         "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    #     },
    # )
    # choreographies: list[Choreography] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "choreography",
    #         "type": "Element",
    #         "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    #     },
    # )
    collaborations: list[Collaboration] = field(
        default_factory=list,
        metadata={
            "name": "collaboration",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    categories: list[Category] = field(
        default_factory=list,
        metadata={
            "name": "category",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    root_elements: list[RootElement] = field(
        default_factory=list,
        metadata={
            "name": "rootElement",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    bpmndiagrams: list[dict] = field(
        default_factory=list,
        metadata={
            "name": "BPMNDiagram",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/DI",
        },
    )
    relationships: list[Relationship] = field(
        default_factory=list,
        metadata={
            "name": "relationship",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    target_namespace: str = field(
        metadata={
            "name": "targetNamespace",
            "type": "Attribute",
            "required": True,
        }
    )
    expression_language: str = field(
        default="http://www.w3.org/1999/XPath",
        metadata={
            "name": "expressionLanguage",
            "type": "Attribute",
        },
    )
    type_language: str = field(
        default="http://www.w3.org/2001/XMLSchema",
        metadata={
            "name": "typeLanguage",
            "type": "Attribute",
        },
    )
    exporter: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    exporter_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "exporterVersion",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "definitions"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[Definitions]:
        """Parse an XML element into a Definitions object."""
        # from pybpmn_parser.bpmn.choreography.choreography import Choreography
        # from pybpmn_parser.bpmn.choreography.global_choreography_task import GlobalChoreographyTask
        from pybpmn_parser.bpmn.activities.global_business_rule_task import GlobalBusinessRuleTask
        from pybpmn_parser.bpmn.activities.global_manual_task import GlobalManualTask
        from pybpmn_parser.bpmn.activities.global_script_task import GlobalScriptTask
        from pybpmn_parser.bpmn.activities.global_user_task import GlobalUserTask
        from pybpmn_parser.bpmn.collaboration.collaboration import Collaboration
        from pybpmn_parser.bpmn.collaboration.participant import PartnerEntity, PartnerRole
        from pybpmn_parser.bpmn.common.category import Category
        from pybpmn_parser.bpmn.common.correlation_property import CorrelationProperty
        from pybpmn_parser.bpmn.common.error import Error
        from pybpmn_parser.bpmn.common.item_definition import ItemDefinition
        from pybpmn_parser.bpmn.common.message import Message
        from pybpmn_parser.bpmn.common.resource import Resource
        from pybpmn_parser.bpmn.conversation.global_conversation import GlobalConversation
        from pybpmn_parser.bpmn.data.data_store import DataStore
        from pybpmn_parser.bpmn.event.escalation import Escalation
        from pybpmn_parser.bpmn.event.signal import Signal
        from pybpmn_parser.bpmn.event_definition.cancel_event_definition import CancelEventDefinition
        from pybpmn_parser.bpmn.event_definition.compensate_event_definition import CompensateEventDefinition
        from pybpmn_parser.bpmn.event_definition.conditional_event_definition import ConditionalEventDefinition
        from pybpmn_parser.bpmn.event_definition.error_event_definition import ErrorEventDefinition
        from pybpmn_parser.bpmn.event_definition.escalation_event_definition import EscalationEventDefinition
        from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
        from pybpmn_parser.bpmn.event_definition.link_event_definition import LinkEventDefinition
        from pybpmn_parser.bpmn.event_definition.message_event_definition import MessageEventDefinition
        from pybpmn_parser.bpmn.event_definition.signal_event_definition import SignalEventDefinition
        from pybpmn_parser.bpmn.event_definition.terminate_event_definition import TerminateEventDefinition
        from pybpmn_parser.bpmn.event_definition.timer_event_definition import TimerEventDefinition
        from pybpmn_parser.bpmn.foundation.base_element import RootElement
        from pybpmn_parser.bpmn.foundation.extension import Extension
        from pybpmn_parser.bpmn.foundation.relationship import Relationship
        from pybpmn_parser.bpmn.infrastructure.import_mod import Import
        from pybpmn_parser.bpmn.process.global_task import GlobalTask
        from pybpmn_parser.bpmn.process.process import Process
        from pybpmn_parser.bpmn.service.end_point import EndPoint
        from pybpmn_parser.bpmn.service.interface import Interface

        if obj is None:
            return None

        attribs = {
            "exporter_version": obj.get("exporterVersion"),
            "exporter": obj.get("exporter"),
            "type_language": obj.get("typeLanguage", "http://www.w3.org/2001/XMLSchema"),
            "expression_language": obj.get("expressionLanguage", "http://www.w3.org/1999/XPath"),
            "target_namespace": obj.get("targetNamespace"),
            "name": obj.get("name"),
            "id": obj.get("id"),
            "relationships": [Relationship.parse(elem) for elem in obj.findall("./bpmn:relationship", NAMESPACES)],
            "bpmndiagrams": [
                xmltodict.parse(ET.tostring(elem)) for elem in obj.findall("./bpmn:BPMNDiagram", NAMESPACES)
            ],
            "root_elements": [RootElement.parse(elem) for elem in obj.findall("./bpmn:rootElement", NAMESPACES)],
            "categories": [Category.parse(elem) for elem in obj.findall("./bpmn:category", NAMESPACES)],
            "collaborations": [Collaboration.parse(elem) for elem in obj.findall("./bpmn:collaboration", NAMESPACES)],
            # "choreographies": [Choreography.parse(elem) for elem in obj.findall("./bpmn:choreography", NAMESPACES)],
            # "global_choreography_tasks": [
            # GlobalChoreographyTask.parse(elem) for elem in obj.findall("./bpmn:globalChoreographyTask", NAMESPACES)
            # ],
            "global_conversations": [
                GlobalConversation.parse(elem) for elem in obj.findall("./bpmn:globalConversation", NAMESPACES)
            ],
            "correlation_properties": [
                CorrelationProperty.parse(elem) for elem in obj.findall("./bpmn:correlationProperty", NAMESPACES)
            ],
            "data_stores": [DataStore.parse(elem) for elem in obj.findall("./bpmn:dataStore", NAMESPACES)],
            "end_points": [EndPoint.parse(elem) for elem in obj.findall("./bpmn:endPoint", NAMESPACES)],
            "errors": [Error.parse(elem) for elem in obj.findall("./bpmn:error", NAMESPACES)],
            "escalations": [Escalation.parse(elem) for elem in obj.findall("./bpmn:escalation", NAMESPACES)],
            "event_definitions": [
                EventDefinition.parse(elem) for elem in obj.findall("./bpmn:eventDefinition", NAMESPACES)
            ],
            "cancel_event_definitions": [
                CancelEventDefinition.parse(elem) for elem in obj.findall("./bpmn:cancelEventDefinition", NAMESPACES)
            ],
            "compensate_event_definitions": [
                CompensateEventDefinition.parse(elem)
                for elem in obj.findall("./bpmn:compensateEventDefinition", NAMESPACES)
            ],
            "conditional_event_definitions": [
                ConditionalEventDefinition.parse(elem)
                for elem in obj.findall("./bpmn:conditionalEventDefinition", NAMESPACES)
            ],
            "error_event_definitions": [
                ErrorEventDefinition.parse(elem) for elem in obj.findall("./bpmn:errorEventDefinition", NAMESPACES)
            ],
            "escalation_event_definitions": [
                EscalationEventDefinition.parse(elem)
                for elem in obj.findall("./bpmn:escalationEventDefinition", NAMESPACES)
            ],
            "link_event_definitions": [
                LinkEventDefinition.parse(elem) for elem in obj.findall("./bpmn:linkEventDefinition", NAMESPACES)
            ],
            "message_event_definitions": [
                MessageEventDefinition.parse(elem) for elem in obj.findall("./bpmn:messageEventDefinition", NAMESPACES)
            ],
            "signal_event_definitions": [
                SignalEventDefinition.parse(elem) for elem in obj.findall("./bpmn:signalEventDefinition", NAMESPACES)
            ],
            "terminate_event_definitions": [
                TerminateEventDefinition.parse(elem)
                for elem in obj.findall("./bpmn:terminateEventDefinition", NAMESPACES)
            ],
            "timer_event_definitions": [
                TimerEventDefinition.parse(elem) for elem in obj.findall("./bpmn:timerEventDefinition", NAMESPACES)
            ],
            "global_business_rule_tasks": [
                GlobalBusinessRuleTask.parse(elem) for elem in obj.findall("./bpmn:globalBusinessRuleTask", NAMESPACES)
            ],
            "global_manual_tasks": [
                GlobalManualTask.parse(elem) for elem in obj.findall("./bpmn:globalManualTask", NAMESPACES)
            ],
            "global_script_tasks": [
                GlobalScriptTask.parse(elem) for elem in obj.findall("./bpmn:globalScriptTask", NAMESPACES)
            ],
            "global_tasks": [GlobalTask.parse(elem) for elem in obj.findall("./bpmn:globalTask", NAMESPACES)],
            "global_user_tasks": [
                GlobalUserTask.parse(elem) for elem in obj.findall("./bpmn:globalUserTask", NAMESPACES)
            ],
            "interfaces": [Interface.parse(elem) for elem in obj.findall("./bpmn:interface", NAMESPACES)],
            "item_definitions": [
                ItemDefinition.parse(elem) for elem in obj.findall("./bpmn:itemDefinition", NAMESPACES)
            ],
            "messages": [Message.parse(elem) for elem in obj.findall("./bpmn:message", NAMESPACES)],
            "partner_entities": [
                PartnerEntity.parse(elem) for elem in obj.findall("./bpmn:partnerEntity", NAMESPACES)
            ],
            "partner_roles": [PartnerRole.parse(elem) for elem in obj.findall("./bpmn:partnerRole", NAMESPACES)],
            "processes": [Process.parse(elem) for elem in obj.findall("./bpmn:process", NAMESPACES)],
            "resources": [Resource.parse(elem) for elem in obj.findall("./bpmn:resource", NAMESPACES)],
            "signals": [Signal.parse(elem) for elem in obj.findall("./bpmn:signal", NAMESPACES)],
            "extensions": [Extension.parse(elem) for elem in obj.findall("./bpmn:extension", NAMESPACES)],
            "imports": [Import.parse(elem) for elem in obj.findall("./bpmn:import", NAMESPACES)],
        }

        return cls(**attribs)
