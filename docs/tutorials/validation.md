# Validating BPMN Documents

This tutorial covers BPMN document validation in PyBPMN Parser.

## Overview

PyBPMN Parser automatically validates BPMN documents against the BPMN 2.0 schema during parsing. This ensures that only valid BPMN documents are processed.

## Automatic Validation

Validation happens automatically when you parse:

```python
from pathlib import Path
from pybpmn_parser.parse import Parser
from pybpmn_parser.validator import ValidationError

# Validation happens automatically
parser = Parser()
try:
    definitions = parser.parse_file(Path("my_process.bpmn"))
    print("✓ Document is valid")
except ValidationError as e:
    print(f"✗ Validation failed: {e}")
```

## Understanding Validation Errors

ValidationError exceptions provide detailed information about what went wrong:

```python
from pybpmn_parser.parse import Parser
from pybpmn_parser.validator import ValidationError

invalid_xml = """<?xml version="1.0"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             targetNamespace="http://bpmn.io/schema/bpmn">
    <process id="proc1">
        <invalidElement id="invalid" />
    </process>
</definitions>"""

try:
    definitions = Parser().parse_string(invalid_xml)
except ValidationError as e:
    print(f"Error: {e}")
    # Error will describe the invalid element
```

## Common Validation Errors

### Empty XML

```python
from pybpmn_parser.validator import validate

result = validate("")
if result.errors:
    # First error will be the empty XML error
    print(result.errors[0])  # "EMPTY_XML: Value cannot be empty"
```

### Invalid Root Element

```python
from pybpmn_parser.validator import validate

invalid_xml = """<?xml version="1.0"?>
<root>
    <child>Invalid</child>
</root>"""

result = validate(invalid_xml)
for err in result.errors:
    print(err)  # SCHEMA_ERROR: ... (root)
```

### Invalid BPMN Elements

```python
from pybpmn_parser.validator import validate

invalid_xml = """<?xml version="1.0"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <invalidTag />
</definitions>"""

result = validate(invalid_xml)
for err in result.errors:
    print(err)  # SCHEMA_ERROR: unexpected child element (definitions)
```

## Manual Validation

You can validate without parsing:

```python
from pybpmn_parser.validator import validate

bpmn_xml = """<?xml version="1.0"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             targetNamespace="http://bpmn.io/schema/bpmn">
    <process id="proc1" />
</definitions>"""

# Validate returns a validation result
result = validate(bpmn_xml)

if result.errors:
    print("Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
else:
    print("✓ Valid BPMN")
```

## Validation Best Practices

### Validate Early

```python
from pathlib import Path
from pybpmn_parser.validator import validate

def validate_file(file_path: Path) -> bool:
    """Validate a BPMN file before processing."""
    xml_content = file_path.read_text(encoding="utf-8")
    result = validate(xml_content)

    if result.errors:
        print(f"Validation failed for {file_path.name}:")
        for error in result.errors:
            print(f"  - {error}")
        return False

    return True

# Validate before parsing
from pybpmn_parser.parse import Parser

if validate_file(Path("my_process.bpmn")):
    parser = Parser()
    definitions = parser.parse_file(Path("my_process.bpmn"))
```

### Batch Validation

```python
from pathlib import Path
from pybpmn_parser.validator import validate

def validate_directory(directory: Path):
    """Validate all BPMN files in a directory."""
    results = {"valid": [], "invalid": []}

    for bpmn_file in directory.glob("*.bpmn"):
        xml_content = bpmn_file.read_text(encoding="utf-8")
        result = validate(xml_content)

        if result.errors:
            results["invalid"].append({
                "file": bpmn_file.name,
                "errors": [str(e) for e in result.errors]
            })
        else:
            results["valid"].append(bpmn_file.name)

    return results

# Validate all files
results = validate_directory(Path("bpmn_models/"))
print(f"Valid: {len(results['valid'])}")
print(f"Invalid: {len(results['invalid'])}")
```

### Handle Validation Gracefully

```python
from pathlib import Path
from pybpmn_parser.parse import Parser
from pybpmn_parser.validator import ValidationError

def safe_parse(file_path: Path):
    """Parse with graceful error handling."""
    parser = Parser()
    try:
        return parser.parse_file(file_path), None
    except ValidationError as e:
        error_msg = {
            "file": str(file_path),
            "error_type": "validation",
            "message": str(e)
        }
        return None, error_msg
    except FileNotFoundError:
        error_msg = {
            "file": str(file_path),
            "error_type": "not_found",
            "message": "File does not exist"
        }
        return None, error_msg

# Use the safe parser
definitions, error = safe_parse(Path("my_process.bpmn"))
if error:
    print(f"Failed: {error['message']}")
else:
    print("Success!")
```

## Custom Validation Rules

While PyBPMN Parser validates against the BPMN schema, you can add custom business rules:

```python
from pathlib import Path
from pybpmn_parser.parse import Parser
from pybpmn_parser.bpmn.event.start_event import StartEvent
from pybpmn_parser.bpmn.event.end_event import EndEvent

def validate_process_structure(process):
    """Custom validation: ensure process has start and end events."""
    errors = []

    # Check for start events
    start_events = [
        el for el in process.flow_elements
        if isinstance(el, StartEvent)
    ]
    if not start_events:
        errors.append(f"Process {process.id} has no start event")

    # Check for end events
    end_events = [
        el for el in process.flow_elements
        if isinstance(el, EndEvent)
    ]
    if not end_events:
        errors.append(f"Process {process.id} has no end event")

    return errors

# Validate structure
parser = Parser()
definitions = parser.parse_file(Path("my_process.bpmn"))
for process in definitions.processes:
    errors = validate_process_structure(process)
    if errors:
        print(f"Structure errors in {process.id}:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"✓ Process {process.id} structure is valid")
```

### Check for Disconnected Elements

```python
from pathlib import Path
from pybpmn_parser.parse import Parser

def find_disconnected_elements(process):
    """Find elements not connected to any sequence flows."""
    disconnected = []

    # Build a set of connected element IDs
    connected = set()
    for flow in process.sequence_flows:
        connected.add(flow.source_ref)
        connected.add(flow.target_ref)

    # Check each flow element
    for element in process.flow_elements:
        if element.id not in connected:
            disconnected.append(element.id)

    return disconnected

parser = Parser()
definitions = parser.parse_file(Path("my_process.bpmn"))
process = definitions.processes[0]

disconnected = find_disconnected_elements(process)
if disconnected:
    print("Disconnected elements:")
    for element_id in disconnected:
        print(f"  - {element_id}")
```

### Validate Naming Conventions

```python
def validate_naming_conventions(process):
    """Ensure elements follow naming conventions."""
    errors = []

    for element in process.flow_elements:
        # Check if element has a name
        if hasattr(element, 'name'):
            if not element.name:
                errors.append(f"Element {element.id} has no name")
            elif len(element.name) < 3:
                errors.append(f"Element {element.id} name too short: {element.name}")

    return errors
```

## Next Steps

- Explore [Vendor Extensions](extensions.md) for working with extended BPMN
- See validation examples in the [Examples Gallery](../examples/index.md)
- Learn about the [API Reference](../reference/index.md) for detailed validation options
