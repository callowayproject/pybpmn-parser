# Working with BPMN Elements

This tutorial explains how to navigate and work with BPMN elements in PyBPMN Parser.

## Overview

BPMN documents contain various types of elements:

- **Flow Elements** - Tasks, events, gateways, and sequence flows
- **Artifacts** - Text annotations, groups, and associations
- **Data Objects** - Data inputs, outputs, and stores
- **Lanes** - Organizational units within pools
- **Collaborations** - Pools and message flows

PyBPMN Parser represents each element type as a Python dataclass with typed attributes.

## Accessing Processes

Start by accessing processes from the definitions:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))

# Iterate through all processes
for process in definitions.processes:
    print(f"Process ID: {process.id}")
    print(f"Process Name: {process.name}")
    print(f"Is Executable: {process.is_executable}")
```

## Working with Flow Elements

Flow elements are the core building blocks of a process:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Iterate through all flow elements
for element in process.flow_elements:
    element_type = element.__class__.__name__
    element_id = element.id
    element_name = getattr(element, 'name', 'N/A')

    print(f"{element_type}: {element_id} - {element_name}")
```

## Finding Specific Element Types

Use `isinstance()` to filter elements by type:

```python
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task
from pybpmn_parser.bpmn.events.start_events import StartEvent
from pybpmn_parser.bpmn.events.end_events import EndEvent
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Find all tasks
tasks = [el for el in process.flow_elements if isinstance(el, Task)]
print(f"Found {len(tasks)} task(s)")

# Find start events
start_events = [el for el in process.flow_elements if isinstance(el, StartEvent)]
print(f"Found {len(start_events)} start event(s)")

# Find end events
end_events = [el for el in process.flow_elements if isinstance(el, EndEvent)]
print(f"Found {len(end_events)} end event(s)")

# Find exclusive gateways
gateways = [el for el in process.flow_elements if isinstance(el, ExclusiveGateway)]
print(f"Found {len(gateways)} exclusive gateway(s)")
```

## Finding Elements by ID

Each element has a unique ID:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

def find_element_by_id(elements, element_id):
    """Find an element by its ID."""
    for element in elements:
        if element.id == element_id:
            return element
    return None

# Find a specific element
task = find_element_by_id(process.flow_elements, "task_1")
if task:
    print(f"Found: {task.name}")
else:
    print("Element not found")
```

## Accessing Element Attributes

Different element types have different attributes:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

for element in process.flow_elements:
    # All elements have an ID
    print(f"ID: {element.id}")

    # Most elements have a name
    if hasattr(element, 'name') and element.name:
        print(f"  Name: {element.name}")

    # Check for documentation
    if hasattr(element, 'documentation') and element.documentation:
        for doc in element.documentation:
            print(f"  Documentation: {doc.text}")

    # Tasks may have additional properties
    if isinstance(element, Task):
        if hasattr(element, 'default') and element.default:
            print(f"  Default Flow: {element.default}")
```

## Working with Sequence Flows

Sequence flows connect elements in a process:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

print("Sequence Flows:")
for flow in process.sequence_flows:
    print(f"  {flow.id}: {flow.source_ref} -> {flow.target_ref}")

    # Some flows have names (especially conditional flows)
    if flow.name:
        print(f"    Name: {flow.name}")

    # Check if it's a conditional flow
    if hasattr(flow, 'condition_expression') and flow.condition_expression:
        print(f"    Condition: Yes")
```

## Building a Process Graph

Create a graph representation of the process flow:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from collections import defaultdict

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Build adjacency list
graph = defaultdict(list)
for flow in process.sequence_flows:
    graph[flow.source_ref].append({
        'target': flow.target_ref,
        'flow_id': flow.id,
        'name': flow.name
    })

# Find outgoing flows for a specific element
element_id = "task_1"
outgoing = graph[element_id]
print(f"Outgoing flows from {element_id}:")
for edge in outgoing:
    print(f"  -> {edge['target']} via {edge['flow_id']}")
```

## Navigating Element Relationships

Find incoming and outgoing flows for an element:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

def get_incoming_flows(process, element_id):
    """Get all incoming sequence flows for an element."""
    return [flow for flow in process.sequence_flows if flow.target_ref == element_id]

def get_outgoing_flows(process, element_id):
    """Get all outgoing sequence flows for an element."""
    return [flow for flow in process.sequence_flows if flow.source_ref == element_id]

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

element_id = "task_1"

incoming = get_incoming_flows(process, element_id)
print(f"Incoming flows: {len(incoming)}")
for flow in incoming:
    print(f"  From: {flow.source_ref}")

outgoing = get_outgoing_flows(process, element_id)
print(f"Outgoing flows: {len(outgoing)}")
for flow in outgoing:
    print(f"  To: {flow.target_ref}")
```

## Working with Gateways

Gateways split and merge process flows:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway
from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Find all gateways
exclusive_gateways = [
    el for el in process.flow_elements
    if isinstance(el, ExclusiveGateway)
]

parallel_gateways = [
    el for el in process.flow_elements
    if isinstance(el, ParallelGateway)
]

print(f"Exclusive Gateways: {len(exclusive_gateways)}")
for gw in exclusive_gateways:
    print(f"  {gw.id}: {gw.name}")

    # Find default flow for decision gateways
    if hasattr(gw, 'default') and gw.default:
        print(f"    Default flow: {gw.default}")

print(f"\nParallel Gateways: {len(parallel_gateways)}")
for gw in parallel_gateways:
    print(f"  {gw.id}: {gw.name}")
```

## Working with Events

Events represent things that happen during process execution:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.events.start_events import StartEvent
from pybpmn_parser.bpmn.events.end_events import EndEvent
from pybpmn_parser.bpmn.events.intermediate_catch_events import IntermediateCatchEvent

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Categorize events
start_events = [el for el in process.flow_elements if isinstance(el, StartEvent)]
end_events = [el for el in process.flow_elements if isinstance(el, EndEvent)]
intermediate_events = [el for el in process.flow_elements if isinstance(el, IntermediateCatchEvent)]

print(f"Start Events: {len(start_events)}")
print(f"End Events: {len(end_events)}")
print(f"Intermediate Events: {len(intermediate_events)}")

# Check event definitions (timers, messages, etc.)
for event in start_events:
    print(f"\nStart Event: {event.id}")
    if hasattr(event, 'event_definitions') and event.event_definitions:
        for event_def in event.event_definitions:
            print(f"  Type: {event_def.__class__.__name__}")
```

## Working with Lanes

Lanes organize elements by role or responsibility:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

if hasattr(process, 'lane_sets') and process.lane_sets:
    for lane_set in process.lane_sets:
        print("Lane Set:")
        for lane in lane_set.lanes:
            print(f"  Lane: {lane.name} (ID: {lane.id})")

            # Elements in this lane
            if hasattr(lane, 'flow_node_refs') and lane.flow_node_refs:
                print(f"    Elements: {len(lane.flow_node_refs)}")
                for element_ref in lane.flow_node_refs:
                    print(f"      - {element_ref}")
```

## Extracting Process Metrics

Calculate useful metrics from the process:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway
from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

def analyze_process(process):
    """Extract metrics from a BPMN process."""
    metrics = {
        'total_elements': len(process.flow_elements),
        'tasks': 0,
        'exclusive_gateways': 0,
        'parallel_gateways': 0,
        'sequence_flows': len(process.sequence_flows),
    }

    for element in process.flow_elements:
        if isinstance(element, Task):
            metrics['tasks'] += 1
        elif isinstance(element, ExclusiveGateway):
            metrics['exclusive_gateways'] += 1
        elif isinstance(element, ParallelGateway):
            metrics['parallel_gateways'] += 1

    # Calculate complexity score
    metrics['complexity_score'] = (
        metrics['tasks'] +
        metrics['exclusive_gateways'] * 2 +  # Decisions add more complexity
        metrics['parallel_gateways'] * 1.5   # Parallelism adds complexity
    )

    return metrics

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

metrics = analyze_process(process)
print(f"Process: {process.id}")
for key, value in metrics.items():
    print(f"  {key}: {value}")
```

## Best Practices

### Use Type Checking

```python
from pybpmn_parser.bpmn.activities.tasks import Task

# Good: Check type before accessing type-specific attributes
if isinstance(element, Task):
    # Safe to access Task-specific attributes
    if element.is_for_compensation:
        print("Compensation task")

# Avoid: Assuming type without checking
# if element.is_for_compensation:  # May raise AttributeError
```

### Handle Missing Attributes

```python
# Good: Use hasattr or getattr
name = getattr(element, 'name', 'Unnamed')
if hasattr(element, 'documentation') and element.documentation:
    print(element.documentation[0].text)

# Avoid: Direct access without checking
# print(element.name)  # May raise AttributeError
```

### Build Helper Functions

```python
def get_element_name(element):
    """Get element name with fallback."""
    if hasattr(element, 'name') and element.name:
        return element.name
    return f"[{element.id}]"

def count_elements_by_type(process):
    """Count elements grouped by type."""
    from collections import Counter
    return Counter(el.__class__.__name__ for el in process.flow_elements)
```

## Next Steps

- Learn about [Validating Documents](validation.md)
- Explore [Vendor Extensions](extensions.md)
- See practical examples in the [Examples Gallery](../examples/index.md)
