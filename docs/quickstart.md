---
title: Quick Start
summary: Get started with PyBPMN Parser in minutes
date: 2025-09-15T12:32:13.355904+00:00
---

# Quick Start

This guide will get you up and running with PyBPMN Parser in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- PyBPMN Parser installed (see [Installation](installation.md))

## Your First BPMN Parse

Let's start by parsing a simple BPMN document:

```python
from pybpmn_parser.parse import parse

# Define a minimal BPMN document
bpmn_xml = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             targetNamespace="http://bpmn.io/schema/bpmn">
    <process id="my_process" name="My First Process">
        <startEvent id="start" name="Start" />
        <task id="task1" name="Do Something" />
        <endEvent id="end" name="End" />
        <sequenceFlow id="flow1" sourceRef="start" targetRef="task1" />
        <sequenceFlow id="flow2" sourceRef="task1" targetRef="end" />
    </process>
</definitions>"""

# Parse the BPMN
definitions = parse(bpmn_xml)

# Access the process
process = definitions.processes[0]
print(f"Process ID: {process.id}")
print(f"Process Name: {process.name}")
print(f"Number of elements: {len(process.flow_elements)}")
```

Expected output:
```
Process ID: my_process
Process Name: My First Process
Number of elements: 3
```

## Parsing from a File

In practice, you'll usually parse BPMN files from disk:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Parse a BPMN file
definitions = parse_file(Path("my_process.bpmn"))

# Iterate through all processes
for process in definitions.processes:
    print(f"\nProcess: {process.id}")

    # List all flow elements (tasks, events, gateways, etc.)
    for element in process.flow_elements:
        element_type = element.__class__.__name__
        element_id = element.id
        element_name = getattr(element, 'name', 'N/A')
        print(f"  {element_type}: {element_id} ({element_name})")
```

## Working with Different Element Types

PyBPMN Parser represents different BPMN elements as distinct Python classes:

```python
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task
from pybpmn_parser.bpmn.events.start_events import StartEvent
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Find specific element types
tasks = [el for el in process.flow_elements if isinstance(el, Task)]
start_events = [el for el in process.flow_elements if isinstance(el, StartEvent)]

print(f"Found {len(tasks)} task(s)")
print(f"Found {len(start_events)} start event(s)")
```

## Validation

PyBPMN Parser automatically validates documents against the BPMN 2.0 schema:

```python
from pybpmn_parser.parse import parse
from pybpmn_parser.validator import ValidationError

# This will raise a ValidationError if the BPMN is invalid
try:
    definitions = parse(bpmn_xml)
    print("✓ BPMN document is valid")
except ValidationError as e:
    print(f"✗ Validation failed: {e}")
```

## Accessing Element Attributes

BPMN elements have attributes you can access directly:

```python
definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

for element in process.flow_elements:
    print(f"Element ID: {element.id}")

    # Many elements have a name attribute
    if hasattr(element, 'name'):
        print(f"  Name: {element.name}")

    # Documentation can be attached to elements
    if hasattr(element, 'documentation'):
        for doc in element.documentation:
            print(f"  Documentation: {doc.text}")
```

## Working with Sequence Flows

Navigate the process flow by following sequence flows:

```python
definitions = parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

# Get all sequence flows
for flow in process.sequence_flows:
    print(f"Flow: {flow.id}")
    print(f"  From: {flow.source_ref}")
    print(f"  To: {flow.target_ref}")
    if flow.name:
        print(f"  Name: {flow.name}")
```

## What's Next?

Now that you've learned the basics, explore these topics:

- **[Parsing Tutorial](tutorials/parsing.md)** - Deep dive into parsing options
- **[Working with Elements](tutorials/elements.md)** - Navigate complex process structures
- **[Validation](tutorials/validation.md)** - Custom validation rules
- **[Examples](examples/index.md)** - Real-world examples with MIWG test files

## Common Patterns

### Loading Multiple Files

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

bpmn_dir = Path("bpmn_models/")
for bpmn_file in bpmn_dir.glob("*.bpmn"):
    try:
        definitions = parse_file(bpmn_file)
        print(f"✓ Parsed {bpmn_file.name}")
    except Exception as e:
        print(f"✗ Failed to parse {bpmn_file.name}: {e}")
```

### Extracting Process Metrics

```python
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.tasks import Task
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("my_process.bpmn"))

for process in definitions.processes:
    task_count = sum(1 for el in process.flow_elements if isinstance(el, Task))
    gateway_count = sum(1 for el in process.flow_elements if isinstance(el, ExclusiveGateway))

    print(f"Process: {process.id}")
    print(f"  Tasks: {task_count}")
    print(f"  Gateways: {gateway_count}")
    print(f"  Complexity: {task_count + gateway_count}")
```

## Troubleshooting

### Common Issues

**ValidationError on parse**: Your BPMN file doesn't conform to the BPMN 2.0 specification. Check the error message for details.

**FileNotFoundError**: Check that the file path is correct and the file exists.

**AttributeError accessing element property**: Not all BPMN elements have all properties. Use `hasattr()` or `getattr()` with defaults.

### Getting Help

- Check the [API Reference](reference/) for detailed documentation
- Browse [Examples](examples/index.md) for working code
- Visit the [GitHub repository](https://github.com/callowayproject/pybpmn-parser) to report issues
