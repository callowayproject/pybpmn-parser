# Plugin Templates

Ready-to-use templates for common plugin patterns.

## Template 1: Basic Namespace Extension

A simple plugin that adds custom attributes to BPMN elements.

```python
"""Basic namespace extension plugin template."""

from typing import Dict, Any
from pybpmn_parser.plugins.registry import register_plugin


class BasicExtensionPlugin:
    """
    Template for basic namespace extension.

    This plugin demonstrates how to:
    - Register a custom namespace
    - Parse custom attributes
    - Provide default values
    """

    # Define your custom namespace
    namespaces = {
        "custom": "http://example.com/custom"
    }

    def __init__(self):
        """Initialize the plugin."""
        self.name = "BasicExtensionPlugin"
        self.version = "1.0.0"

    def parse_extension(
        self,
        element,
        extension_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse custom extension attributes.

        Args:
            element: The BPMN element being parsed
            extension_data: Raw extension data from XML

        Returns:
            Dictionary of parsed extension attributes
        """
        parsed = {}

        namespace_uri = "http://example.com/custom"

        for key, value in extension_data.items():
            # Check if attribute is from our namespace
            if namespace_uri in key:
                # Extract attribute name (remove namespace prefix)
                attr_name = key.split("}")[-1]
                parsed[attr_name] = value

        return parsed


# Register the plugin
if __name__ == "__main__":
    register_plugin(BasicExtensionPlugin())
```

### Usage Example

```xml
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:custom="http://example.com/custom">
    <process id="proc1">
        <task id="task1" custom:priority="high" custom:cost="100" />
    </process>
</definitions>
```

```python
from pybpmn_parser.parse import parse_file
from pathlib import Path

# Parse BPMN with custom extensions
definitions = parse_file(Path("custom_process.bpmn"))
```

## Template 2: Vendor-Specific Plugin (Camunda-Style)

Plugin template for vendor-specific extensions like Camunda.

```python
"""Vendor-specific plugin template (Camunda-style)."""

from typing import Dict, Any, List
from pybpmn_parser.plugins.registry import register_plugin


class VendorPlugin:
    """
    Template for vendor-specific extensions.

    Demonstrates:
    - Multiple namespace support
    - Complex attribute parsing
    - Validation rules
    - Extension elements handling
    """

    namespaces = {
        "vendor": "http://vendor.com/bpmn",
        "vendor-ext": "http://vendor.com/extensions"
    }

    def __init__(self):
        """Initialize the plugin."""
        self.name = "VendorPlugin"
        self.version = "1.0.0"
        self.vendor = "Vendor Corp"

    def parse_extension(
        self,
        element,
        extension_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse vendor-specific extensions."""
        parsed = {
            'async_before': False,
            'async_after': False,
            'exclusive': True,
            'job_priority': None,
            'properties': {}
        }

        namespace_uri = "http://vendor.com/bpmn"

        for key, value in extension_data.items():
            if namespace_uri not in key:
                continue

            attr_name = key.split("}")[-1]

            if attr_name == "asyncBefore":
                parsed['async_before'] = value.lower() == "true"
            elif attr_name == "asyncAfter":
                parsed['async_after'] = value.lower() == "true"
            elif attr_name == "exclusive":
                parsed['exclusive'] = value.lower() == "true"
            elif attr_name == "jobPriority":
                parsed['job_priority'] = int(value)
            else:
                parsed['properties'][attr_name] = value

        return parsed

    def validate_extension(
        self,
        element,
        extension_data: Dict[str, Any]
    ) -> List[str]:
        """Validate vendor-specific extensions."""
        errors = []

        # Validate job priority range
        if extension_data.get('job_priority'):
            priority = extension_data['job_priority']
            if priority < 0 or priority > 100:
                errors.append(
                    f"Element {element.id}: job_priority must be 0-100"
                )

        # Validate async configuration
        async_before = extension_data.get('async_before', False)
        async_after = extension_data.get('async_after', False)

        if async_before and async_after:
            errors.append(
                f"Element {element.id}: cannot have both asyncBefore "
                "and asyncAfter"
            )

        return errors


# Register the plugin
if __name__ == "__main__":
    register_plugin(VendorPlugin())
```

### Usage Example

```xml
<serviceTask id="task1"
             vendor:asyncBefore="true"
             vendor:jobPriority="50"
             vendor:class="com.example.MyDelegate" />
```

## Template 3: Custom Validation Plugin

Plugin focused on adding custom validation rules.

```python
"""Custom validation plugin template."""

from typing import Dict, Any, List
from pybpmn_parser.plugins.registry import register_plugin


class ValidationPlugin:
    """
    Template for custom validation rules.

    Demonstrates:
    - Process-level validation
    - Element-level validation
    - Business rule validation
    - Naming convention checks
    """

    namespaces = {
        "validate": "http://example.com/validation"
    }

    def __init__(self):
        """Initialize the plugin."""
        self.name = "ValidationPlugin"
        self.version = "1.0.0"
        self.validation_rules = []

    def parse_extension(
        self,
        element,
        extension_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse validation annotations."""
        validation_config = {
            'required_fields': [],
            'naming_pattern': None,
            'max_duration': None
        }

        namespace_uri = "http://example.com/validation"

        for key, value in extension_data.items():
            if namespace_uri not in key:
                continue

            attr_name = key.split("}")[-1]

            if attr_name == "requiredFields":
                validation_config['required_fields'] = value.split(",")
            elif attr_name == "namingPattern":
                validation_config['naming_pattern'] = value
            elif attr_name == "maxDuration":
                validation_config['max_duration'] = value

        return validation_config

    def validate_process(self, process) -> List[str]:
        """Validate entire process."""
        errors = []

        # Rule 1: Process must have start and end events
        from pybpmn_parser.bpmn.events.start_events import StartEvent
        from pybpmn_parser.bpmn.events.end_events import EndEvent

        start_events = [
            el for el in process.flow_elements
            if isinstance(el, StartEvent)
        ]
        end_events = [
            el for el in process.flow_elements
            if isinstance(el, EndEvent)
        ]

        if not start_events:
            errors.append(f"Process {process.id} has no start event")
        if not end_events:
            errors.append(f"Process {process.id} has no end event")

        # Rule 2: All elements must have names
        for element in process.flow_elements:
            if hasattr(element, 'name'):
                if not element.name or element.name.strip() == "":
                    errors.append(
                        f"Element {element.id} has no name"
                    )

        # Rule 3: No disconnected elements
        connected_ids = set()
        for flow in process.sequence_flows:
            connected_ids.add(flow.source_ref)
            connected_ids.add(flow.target_ref)

        for element in process.flow_elements:
            if element.id not in connected_ids:
                errors.append(
                    f"Element {element.id} is not connected to any flow"
                )

        return errors

    def validate_element(self, element) -> List[str]:
        """Validate individual element."""
        errors = []

        # Check naming conventions
        if hasattr(element, 'name') and element.name:
            # Rule: Names should be title case
            if not element.name[0].isupper():
                errors.append(
                    f"Element {element.id} name should start "
                    f"with uppercase: {element.name}"
                )

            # Rule: Names should be under 50 characters
            if len(element.name) > 50:
                errors.append(
                    f"Element {element.id} name too long (>50 chars)"
                )

        return errors


# Register the plugin
if __name__ == "__main__":
    register_plugin(ValidationPlugin())
```

### Usage

```python
from pybpmn_parser.parse import parse_file
from pathlib import Path

# Parse and validate
definitions = parse_file(Path("process.bpmn"))
process = definitions.processes[0]

# Run custom validation
plugin = ValidationPlugin()
errors = plugin.validate_process(process)

if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

## Using These Templates

### 1. Copy and Customize

Copy a template and modify it for your needs:

```python
# Copy BasicExtensionPlugin template
# Change namespace to your domain
namespaces = {
    "mycompany": "http://mycompany.com/bpmn"
}

# Customize parsing logic
def parse_extension(self, element, extension_data):
    # Your custom logic here
    pass
```

### 2. Combine Templates

Mix features from multiple templates:

```python
class MyCustomPlugin(BasicExtensionPlugin, ValidationPlugin):
    """Plugin combining extension parsing and validation."""

    namespaces = {
        "custom": "http://example.com/custom",
        "validate": "http://example.com/validation"
    }
```

### 3. Test Your Plugin

```python
import pytest
from pathlib import Path
from pybpmn_parser.parse import parse_file

def test_custom_plugin():
    """Test custom plugin functionality."""
    test_file = Path("tests/fixtures/custom_process.bpmn")
    definitions = parse_file(test_file)

    # Verify plugin parsed extensions
    process = definitions.processes[0]
    task = process.flow_elements[0]

    assert hasattr(task, 'custom_attribute')
```

## Next Steps

- Read [Creating Plugins](creating.md) for detailed guidance
- Review [Best Practices](best-practices.md) for recommendations
- Check the [API Reference](../reference/) for plugin system details
