# Sequential Flow Example

This example demonstrates parsing a simple sequential BPMN process using the MIWG test suite file A.1.0.bpmn.

## Overview

Sequential flow is the simplest BPMN pattern where tasks execute one after another in a linear sequence.

## BPMN Diagram

This example uses the MIWG test file `A.1.0.bpmn` which contains a basic sequential process.

## Python Code

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Parse the BPMN file
bpmn_file = Path("tests/fixtures/miwg-test-suite-2025/A.1.0.bpmn")
definitions = parse_file(bpmn_file)

# Access the process
process = definitions.processes[0]
print(f"Process: {process.id}")
print(f"Name: {process.name}")

# List all flow elements
print("\nFlow Elements:")
for element in process.flow_elements:
    element_type = element.__class__.__name__
    element_id = element.id
    element_name = getattr(element, 'name', 'N/A')
    print(f"  {element_type}: {element_id} ({element_name})")

# List sequence flows
print("\nSequence Flows:")
for flow in process.sequence_flows:
    print(f"  {flow.id}: {flow.source_ref} -> {flow.target_ref}")
```

## Expected Output

```
Process: _6-1
Name: A.1.0

Flow Elements:
  StartEvent: _6-61 (Start Event)
  Task: _6-74 (Task 1)
  Task: _6-125 (Task 2)
  Task: _6-178 (Task 3)
  EndEvent: _6-219 (End Event)

Sequence Flows:
  _6-125: _6-61 -> _6-74
  _6-178: _6-74 -> _6-125
  _6-219: _6-125 -> _6-178
  _6-438: _6-178 -> _6-219
```

## Variations

### Finding the Execution Path

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.1.0.bpmn"))
process = definitions.processes[0]

# Build a simple execution path
def build_execution_path(process):
    """Build the execution path from start to end."""
    # Find start event
    from pybpmn_parser.bpmn.events.start_events import StartEvent
    start_events = [el for el in process.flow_elements if isinstance(el, StartEvent)]

    if not start_events:
        return []

    path = [start_events[0].id]
    current_id = start_events[0].id

    # Follow sequence flows
    visited = set()
    while current_id and current_id not in visited:
        visited.add(current_id)

        # Find outgoing flow
        outgoing = [f for f in process.sequence_flows if f.source_ref == current_id]
        if outgoing:
            next_id = outgoing[0].target_ref
            path.append(next_id)
            current_id = next_id
        else:
            break

    return path

path = build_execution_path(process)
print("Execution Path:", " -> ".join(path))
```

### Extracting Task Names

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.1.0.bpmn"))
process = definitions.processes[0]

# Extract all tasks
tasks = [el for el in process.flow_elements if isinstance(el, Task)]

print("Tasks in process:")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task.name} (ID: {task.id})")
```

## Key Concepts

- **Sequential Flow**: Tasks execute in a defined order
- **Sequence Flows**: Connect elements to define execution order
- **Start Event**: Where the process begins
- **End Event**: Where the process completes

## Next Steps

- Explore [Parallel Gateway](parallel-gateway.md) for concurrent execution
- Learn about [Exclusive Gateway](exclusive-gateway.md) for conditional branching
- Check [Working with Elements](../tutorials/elements.md) for more navigation techniques
