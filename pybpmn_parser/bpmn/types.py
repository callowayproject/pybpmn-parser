"""Types used in the BPMN specification."""

from __future__ import annotations

from enum import StrEnum, auto


class ImplementationValue(StrEnum):
    """Specifies the technology that will be used to send and receive the Messages."""

    UNSPECIFIED = "##unspecified"
    WEB_SERVICE = "##WebService"


class MultiInstanceFlowCondition(StrEnum):
    """The behavior of a multi-instance loop."""

    NONE = "None"
    ONE = "One"
    ALL = "All"
    COMPLEX = "Complex"


class AdHocOrdering(StrEnum):
    """This attribute defines if the Activities within the Process can be performed in parallel or sequentially."""

    PARALLEL = "Parallel"
    SEQUENTIAL = "Sequential"


class TransactionMethodValue(StrEnum):
    """Defines the Transaction method used to commit or cancel a Transaction."""

    COMPENSATE = "##Compensate"
    IMAGE = "##Image"
    STORE = "##Store"


class ItemKind(StrEnum):
    """Specifies the nature of an item, which can be a physical or information item."""

    INFORMATION = "Information"
    PHYSICAL = "Physical"


class ProcessType(StrEnum):
    """Provides additional information about the level of abstraction modeled by this Process."""

    NONE = "None"
    PUBLIC = "Public"
    PRIVATE = "Private"


class ChoreographyLoopType(StrEnum):
    """Determines the appropriate marker for a Choreography Activity that repeats."""

    NONE = "None"
    STANDARD = "Standard"
    MULTI_INSTANCE_SEQUENTIAL = "MultiInstanceSequential"
    MULTI_INSTANCE_PARALLEL = "MultiInstanceParallel"


class AssociationDirection(StrEnum):
    """Defines whether the Association shows any directionality with an arrowhead."""

    NONE = "None"
    ONE = "One"
    BOTH = "Both"


class GatewayDirection(StrEnum):
    """
    Constraints on how the Gateway MAY be used.

    • Unspecified: There are no constraints. The Gateway MAY have any number of incoming and outgoing Sequence Flows.
    • Converging: This Gateway MAY have multiple incoming Sequence Flows but MUST have no more than
        one (1) outgoing Sequence Flow.
    • Diverging: This Gateway MAY have multiple outgoing Sequence Flows but MUST have no more than
        one (1) incoming Sequence Flow.
    • Mixed: This Gateway contains multiple outgoing and multiple incoming Sequence Flows.
    """

    UNSPECIFIED = "Unspecified"
    CONVERGING = "Converging"
    DIVERGING = "Diverging"
    MIXED = "Mixed"


class EventBasedGatewayType(StrEnum):
    """Determines the behavior of the Gateway when used to instantiate a Process."""

    EXCLUSIVE = "Exclusive"
    PARALLEL = "Parallel"


class RelationshipDirection(StrEnum):
    """This attribute specifies the direction of a relationship."""

    NONE = "None"
    FORWARD = "Forward"
    BACKWARD = "Backward"
    BOTH = "Both"


class StartEventType(StrEnum):
    """This attribute specifies the type of Start Event."""

    NONE = auto()
    MESSAGE = auto()
    TIMER = auto()
    CONDITIONAL = auto()
    SIGNAL = auto()
    MULTIPLE = auto()
    PARALLEL_MULTIPLE = auto()
    ESCALATION = auto()
    ERROR = auto()
    COMPENSATION = auto()
    UNKNOWN = auto()


NAMESPACES = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
