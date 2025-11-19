"""Unit tests for the StartEvent class."""

from pybpmn_parser.bpmn.event.start_event import StartEvent
from pybpmn_parser.bpmn.types import StartEventType


class TestStartEventType:
    """Unit tests for the StartEvent class's event_type property."""

    def test_event_type_none(self):
        """Test when there are no event definitions."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.NONE

    def test_event_type_message(self):
        """Test when there is only a message event definition."""
        start_event = StartEvent(
            message_event_definition=[object()],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.MESSAGE

    def test_event_type_timer(self):
        """Test when there is only a timer event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[object()],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.TIMER

    def test_event_type_conditional(self):
        """Test when there is only a conditional event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[object()],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.CONDITIONAL

    def test_event_type_signal(self):
        """Test when there is only a signal event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[object()],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.SIGNAL

    def test_event_type_multiple(self):
        """Test when there are multiple event definitions."""
        start_event = StartEvent(
            message_event_definition=[object()],
            timer_event_definition=[object()],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
            parallel_multiple=False,
        )
        assert start_event.event_type == StartEventType.MULTIPLE

    def test_event_type_parallel_multiple(self):
        """Test when there are multiple event definitions and parallel_multiple is True."""
        start_event = StartEvent(
            message_event_definition=[object()],
            timer_event_definition=[object()],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
            parallel_multiple=True,
        )
        assert start_event.event_type == StartEventType.PARALLEL_MULTIPLE

    def test_event_type_escalation(self):
        """Test when there is only an escalation event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[object()],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.ESCALATION

    def test_event_type_error(self):
        """Test when there is only an error event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[object()],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.ERROR

    def test_event_type_compensation(self):
        """Test when there is only a compensation event definition."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[object()],
            error_event_definition=[],
            event_definition=[],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.COMPENSATION

    def test_event_type_unknown(self):
        """Test when there is an unknown event type."""
        start_event = StartEvent(
            message_event_definition=[],
            timer_event_definition=[],
            conditional_event_definition=[],
            signal_event_definition=[],
            escalation_event_definition=[],
            compensate_event_definition=[],
            error_event_definition=[],
            event_definition=[object()],
            event_definition_ref=[],
        )
        assert start_event.event_type == StartEventType.UNKNOWN
