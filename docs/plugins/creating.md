# Creating Plugins

This guide explains how to create plugins for PyBPMN Parser to support custom BPMN extensions.

## Plugin Basics

Plugins extend PyBPMN Parser to handle vendor-specific BPMN extensions. A plugin typically:

1. Registers custom XML namespaces
2. Defines how to parse extension elements
3. Extends BPMN element classes with custom attributes
4. Optionally adds custom validation rules

## Plugin Structure

A basic plugin is a Python class that implements the plugin interface:

```python
class MyCustomPlugin:
    """Plugin for custom BPMN extensions."""

    # Define the namespaces this plugin handles
    namespaces = {
        "custom": "http://example.com/custom"
    }

    def parse_extension(self, element, extension_data):
        """Parse custom extension data."""
        # Implementation here
        return extension_data
```

## Creating Your First Plugin

### Step 1: Define the Plugin Class

```python
from typing import Dict, Any

class SimpleExtensionPlugin:
    """Simple plugin for custom namespace support."""

    # Namespace mapping
    namespaces = {
        "myns": "http://example.com/myns"
    }

    def __init__(self):
        """Initialize the plugin."""
        self.name = "SimpleExtensionPlugin"
        self.version = "1.0.0"
```

### Step 2: Implement Extension Parsing

```python
class SimpleExtensionPlugin:
    namespaces = {
        "myns": "http://example.com/myns"
    }

    def parse_extension(self, element, extension_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse custom extension attributes.

        Args:
            element: The BPMN element being parsed
            extension_data: Dictionary of extension attributes

        Returns:
            Processed extension data
        """
        # Extract attributes from your namespace
        custom_attrs = {}

        for key, value in extension_data.items():
            if key.startswith("{http://example.com/myns}"):
                # Remove namespace prefix
                clean_key = key.split("}")[1]
                custom_attrs[clean_key] = value

        return custom_attrs
```

### Step 3: Register the Plugin

```python
from pybpmn_parser.plugins.registry import register_plugin

# Create and register plugin instance
plugin = SimpleExtensionPlugin()
register_plugin(plugin)
```

## Complete Plugin Example

Here's a complete working plugin:

```python
from typing import Dict, Any, Optional
from pybpmn_parser.plugins.registry import register_plugin

class DocumentationPlugin:
    """Plugin that adds enhanced documentation support."""

    namespaces = {
        "doc": "http://example.com/documentation"
    }

    def __init__(self):
        self.name = "DocumentationPlugin"
        self.version = "1.0.0"

    def parse_extension(self, element, extension_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse documentation extension attributes."""
        doc_data = {}

        for key, value in extension_data.items():
            if "{http://example.com/documentation}" in key:
                attr_name = key.split("}")[1]
                doc_data[attr_name] = value

        return doc_data

    def validate_extension(self, element, extension_data: Dict[str, Any]) -> list:
        """Validate extension data."""
        errors = []

        # Example validation: check required attributes
        if extension_data and "author" not in extension_data:
            errors.append(f"Element {element.id} missing required 'author' attribute")

        return errors

# Register the plugin
register_plugin(DocumentationPlugin())
```

## Advanced Plugin Features

### Extending Element Classes

Plugins can add new attributes to BPMN element classes:

```python
class EnhancedTaskPlugin:
    """Plugin that extends task elements."""

    namespaces = {
        "enhanced": "http://example.com/enhanced"
    }

    def extend_element(self, element_class):
        """Add custom attributes to element class."""
        # This is a conceptual example
        # Actual implementation depends on the plugin system

        original_init = element_class.__init__

        def enhanced_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.priority = None
            self.cost = None

        element_class.__init__ = enhanced_init
        return element_class
```

### Custom Validation Rules

Add validation logic specific to your extensions:

```python
class ValidationPlugin:
    """Plugin with custom validation rules."""

    namespaces = {
        "validation": "http://example.com/validation"
    }

    def validate_process(self, process):
        """Validate entire process."""
        errors = []

        # Custom rule: all tasks must have priority
        for element in process.flow_elements:
            if hasattr(element, 'task_type'):
                if not hasattr(element, 'priority'):
                    errors.append(
                        f"Task {element.id} missing priority attribute"
                    )

        return errors
```

## Plugin Best Practices

### 1. Use Descriptive Names

```python
# Good: Clear and descriptive
class CamundaWorkflowPlugin:
    pass

# Avoid: Vague or generic
class Plugin1:
    pass
```

### 2. Version Your Plugins

```python
class MyPlugin:
    def __init__(self):
        self.name = "MyPlugin"
        self.version = "1.0.0"
        self.supported_bpmn_version = "2.0"
```

### 3. Document Extension Attributes

```python
class DocumentedPlugin:
    """
    Plugin for custom extensions.

    Supported Attributes:
        - myns:priority (string): Task priority level
        - myns:cost (float): Estimated task cost
        - myns:owner (string): Task owner identifier

    Example BPMN:
        <task id="task1" myns:priority="high" myns:cost="100.0">
    """

    namespaces = {
        "myns": "http://example.com/myns"
    }
```

### 4. Handle Missing Data Gracefully

```python
def parse_extension(self, element, extension_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse with default values."""
    parsed = {
        'priority': extension_data.get('priority', 'normal'),
        'cost': extension_data.get('cost', 0.0),
        'owner': extension_data.get('owner', 'unassigned')
    }
    return parsed
```

### 5. Validate Input Data

```python
def parse_extension(self, element, extension_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and validate extension data."""
    parsed = {}

    # Validate priority values
    priority = extension_data.get('priority')
    if priority and priority not in ['low', 'normal', 'high']:
        raise ValueError(f"Invalid priority: {priority}")

    parsed['priority'] = priority
    return parsed
```

## Testing Your Plugin

Always test your plugin with real BPMN files:

```python
import pytest
from pathlib import Path
from pybpmn_parser.parse import parse_file

def test_my_plugin():
    """Test plugin with sample BPMN file."""
    # Create test BPMN with your extension
    test_bpmn = Path("test_files/extended_process.bpmn")

    # Parse with plugin
    definitions = parse_file(test_bpmn)

    # Verify extension data was parsed
    process = definitions.processes[0]
    task = process.flow_elements[0]

    assert hasattr(task, 'priority')
    assert task.priority == 'high'
```

## Plugin Distribution

### As a Python Package

Structure your plugin as a package:

```
my_bpmn_plugin/
├── pyproject.toml
├── README.md
├── src/
│   └── my_bpmn_plugin/
│       ├── __init__.py
│       └── plugin.py
└── tests/
    └── test_plugin.py
```

### Installation

Users can install your plugin:

```bash
pip install my-bpmn-plugin
```

### Auto-Registration

Plugins can auto-register on import:

```python
# my_bpmn_plugin/__init__.py
from pybpmn_parser.plugins.registry import register_plugin
from .plugin import MyPlugin

# Auto-register when package is imported
register_plugin(MyPlugin())
```

## Next Steps

- Review [Plugin Templates](templates.md) for ready-to-use examples
- Check [Best Practices](best-practices.md) for recommendations
- Explore the [API Reference](../reference/) for plugin system details
