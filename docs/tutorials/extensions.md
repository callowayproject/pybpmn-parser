# Working with Vendor Extensions

This tutorial covers how to work with vendor-specific BPMN extensions in PyBPMN Parser.

## Overview

Many BPMN modeling tools add vendor-specific extensions to the BPMN standard. PyBPMN Parser supports these extensions through its plugin system.

Common vendor extensions include:

- **Camunda** - Process automation platform extensions
- **Activiti** - Workflow engine extensions
- **jBPM** - Business process management extensions

## Understanding Extensions

Vendor extensions use custom XML namespaces to add attributes and elements beyond the BPMN 2.0 standard:

```xml
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:camunda="http://camunda.org/schema/1.0/bpmn">
    <process id="process1">
        <serviceTask id="task1" camunda:asyncBefore="true">
    </process>
</definitions>
```

## Parsing Files with Extensions

PyBPMN Parser automatically handles vendor extensions:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Parse BPMN with Camunda extensions
definitions = parse_file(Path("camunda_process.bpmn"))

# Extensions are preserved in the element
process = definitions.processes[0]
for element in process.flow_elements:
    print(f"Element: {element.id}")

    # Extension elements are available
    if hasattr(element, 'extension_elements'):
        print(f"  Has extensions: {element.extension_elements is not None}")
```

## Accessing Extension Elements

Extension elements contain vendor-specific data:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("extended_process.bpmn"))
process = definitions.processes[0]

for element in process.flow_elements:
    if hasattr(element, 'extension_elements') and element.extension_elements:
        print(f"Element {element.id} has extensions:")

        # Extension elements contain vendor-specific data
        ext_elements = element.extension_elements
        print(f"  Extension data: {ext_elements}")
```

## Working with Camunda Extensions

Camunda is one of the most popular BPMN platforms:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Parse a BPMN file with Camunda extensions
definitions = parse_file(Path("camunda_process.bpmn"))
process = definitions.processes[0]

for element in process.flow_elements:
    # Check for Camunda-specific attributes
    if hasattr(element, 'extension_elements') and element.extension_elements:
        print(f"Element {element.id}:")

        # Camunda extensions might include:
        # - Task listeners
        # - Execution listeners
        # - Input/output mappings
        # - Form fields
        print(f"  Extensions: {element.extension_elements}")
```

## Custom Namespace Handling

Access attributes from custom namespaces:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
import lxml.etree as ET

def get_namespace_attributes(element, namespace):
    """Get all attributes from a specific namespace."""
    # This is a conceptual example
    # Actual implementation depends on how extensions are stored
    if hasattr(element, 'extension_elements'):
        return element.extension_elements
    return {}

definitions = parse_file(Path("extended_process.bpmn"))
process = definitions.processes[0]

for element in process.flow_elements:
    # Get Camunda-specific attributes
    camunda_attrs = get_namespace_attributes(element, "camunda")
    if camunda_attrs:
        print(f"Camunda attributes for {element.id}:")
        print(f"  {camunda_attrs}")
```

## Checking for Specific Extensions

Detect which extensions are present:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

def detect_extensions(definitions):
    """Detect which vendor extensions are used."""
    extensions = set()

    # Check definitions namespaces
    if hasattr(definitions, 'namespaces'):
        for ns_prefix, ns_uri in definitions.namespaces.items():
            if 'camunda' in ns_uri:
                extensions.add('Camunda')
            elif 'activiti' in ns_uri:
                extensions.add('Activiti')
            elif 'jbpm' in ns_uri:
                extensions.add('jBPM')

    return extensions

definitions = parse_file(Path("extended_process.bpmn"))
extensions = detect_extensions(definitions)

if extensions:
    print(f"Detected extensions: {', '.join(extensions)}")
else:
    print("No vendor extensions detected")
```

## Extension Best Practices

### Check for Extensions First

```python
def has_extensions(element):
    """Check if an element has extensions."""
    return (
        hasattr(element, 'extension_elements') and
        element.extension_elements is not None
    )

for element in process.flow_elements:
    if has_extensions(element):
        # Process extensions
        pass
```

### Handle Missing Extensions Gracefully

```python
def get_extension_value(element, key, default=None):
    """Safely get an extension value."""
    if not has_extensions(element):
        return default

    # Extract value from extensions
    # Implementation depends on extension structure
    return default

# Use with fallback
async_before = get_extension_value(element, 'asyncBefore', False)
```

### Document Extension Usage

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

def document_extensions(process):
    """Create a report of extension usage."""
    report = {
        'elements_with_extensions': 0,
        'extension_types': set()
    }

    for element in process.flow_elements:
        if has_extensions(element):
            report['elements_with_extensions'] += 1

            # Analyze extension types
            # (Implementation depends on extension structure)

    return report

definitions = parse_file(Path("extended_process.bpmn"))
process = definitions.processes[0]

report = document_extensions(process)
print(f"Elements with extensions: {report['elements_with_extensions']}")
```

## Creating Custom Extensions

You can create plugins to handle custom extensions. See the [Plugin Development Guide](../plugins/index.md) for details:

```python
# Example plugin structure
class CustomExtensionPlugin:
    """Plugin for custom BPMN extensions."""

    namespaces = {
        "custom": "http://example.com/custom"
    }

    def parse_extension(self, element, extension_data):
        """Parse custom extension data."""
        # Implementation here
        pass
```

## Working with Multiple Extensions

A BPMN file can have multiple vendor extensions:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("multi_vendor_process.bpmn"))

# Check what extensions are present
if hasattr(definitions, 'extensions'):
    print("Extensions found:")
    for ext in definitions.extensions:
        print(f"  - {ext}")

# Process elements based on which extensions are present
process = definitions.processes[0]
for element in process.flow_elements:
    if has_extensions(element):
        # Handle each extension type appropriately
        print(f"Element {element.id} uses extensions")
```

## Real-World Example: Processing Camunda Tasks

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.activities.service_tasks import ServiceTask

def extract_camunda_task_info(task):
    """Extract Camunda-specific information from a task."""
    info = {
        'id': task.id,
        'name': task.name,
        'has_extensions': False
    }

    if hasattr(task, 'extension_elements') and task.extension_elements:
        info['has_extensions'] = True
        # Parse Camunda-specific attributes
        # (Implementation depends on Camunda extension structure)

    return info

definitions = parse_file(Path("camunda_process.bpmn"))
process = definitions.processes[0]

# Find all service tasks
service_tasks = [
    el for el in process.flow_elements
    if isinstance(el, ServiceTask)
]

# Extract Camunda configuration
for task in service_tasks:
    info = extract_camunda_task_info(task)
    print(f"Service Task: {info['name']}")
    print(f"  Has Camunda extensions: {info['has_extensions']}")
```

## Next Steps

- Learn how to create plugins in the [Plugin Development Guide](../plugins/index.md)
- See extension examples in the [Examples Gallery](../examples/index.md)
- Check the [API Reference](../reference/index.md) for extension-related classes
