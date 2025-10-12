# Plugin Best Practices

Best practices and recommendations for developing PyBPMN Parser plugins.

## Naming Conventions

### Plugin Classes

Use descriptive, specific names:

```python
# Good: Clear and specific
class CamundaWorkflowPlugin:
    pass

class JiraIntegrationPlugin:
    pass

# Avoid: Vague or generic
class Plugin1:
    pass

class MyPlugin:
    pass
```

### Namespace Prefixes

Choose meaningful namespace prefixes:

```python
# Good: Clear purpose
namespaces = {
    "camunda": "http://camunda.org/schema/1.0/bpmn",
    "workflow": "http://mycompany.com/workflow",
    "jira": "http://mycompany.com/jira"
}

# Avoid: Generic or unclear
namespaces = {
    "ns1": "http://example.com/schema",
    "x": "http://example.com/x"
}
```

### Attribute Names

Use camelCase for BPMN compatibility:

```python
# Good: BPMN standard camelCase
extension_data = {
    'asyncBefore': True,
    'jobPriority': 50,
    'retryTimeCycle': "R3/PT5M"
}

# Avoid: Python snake_case in XML
extension_data = {
    'async_before': True,  # Wrong for XML attributes
    'job_priority': 50
}
```

## Version Compatibility

### Document Supported Versions

```python
class MyPlugin:
    """
    My Custom Plugin

    Compatibility:
        - PyBPMN Parser: >= 1.0.0
        - BPMN: 2.0
        - Python: >= 3.8

    Version History:
        - 1.0.0: Initial release
        - 1.1.0: Added validation support
    """

    def __init__(self):
        self.version = "1.1.0"
        self.min_bpmn_parser_version = "1.0.0"
```

### Check Version Compatibility

```python
from packaging import version

class MyPlugin:
    def __init__(self):
        self.version = "1.0.0"
        self.check_compatibility()

    def check_compatibility(self):
        """Check if plugin is compatible with current environment."""
        import pybpmn_parser

        min_version = "1.0.0"
        current = pybpmn_parser.__version__

        if version.parse(current) < version.parse(min_version):
            raise RuntimeError(
                f"Plugin requires pybpmn-parser >= {min_version}, "
                f"found {current}"
            )
```

## Error Handling

### Validate Input Data

```python
def parse_extension(self, element, extension_data):
    """Parse with validation."""
    parsed = {}

    # Validate data types
    priority = extension_data.get('priority')
    if priority:
        if priority not in ['low', 'medium', 'high']:
            raise ValueError(
                f"Invalid priority '{priority}' for element {element.id}. "
                f"Must be one of: low, medium, high"
            )
        parsed['priority'] = priority

    # Validate numeric ranges
    cost = extension_data.get('cost')
    if cost:
        try:
            cost_value = float(cost)
            if cost_value < 0:
                raise ValueError("Cost cannot be negative")
            parsed['cost'] = cost_value
        except ValueError as e:
            raise ValueError(
                f"Invalid cost value for element {element.id}: {e}"
            )

    return parsed
```

### Provide Helpful Error Messages

```python
# Good: Specific and actionable
raise ValueError(
    f"Element '{element.id}' has invalid priority '{priority}'. "
    f"Valid values are: 'low', 'medium', 'high'"
)

# Avoid: Vague or unhelpful
raise ValueError("Invalid value")
```

### Use Warnings for Non-Critical Issues

```python
import warnings

def parse_extension(self, element, extension_data):
    """Parse with warnings for deprecated features."""
    parsed = {}

    # Warn about deprecated attributes
    if 'oldAttribute' in extension_data:
        warnings.warn(
            f"Attribute 'oldAttribute' in element {element.id} is deprecated. "
            f"Use 'newAttribute' instead.",
            DeprecationWarning
        )
        parsed['newAttribute'] = extension_data['oldAttribute']

    return parsed
```

## Testing

### Write Comprehensive Tests

```python
import pytest
from pathlib import Path
from pybpmn_parser.parse import parse_file

class TestMyPlugin:
    """Test suite for MyPlugin."""

    def test_parse_basic_attributes(self):
        """Test parsing basic extension attributes."""
        bpmn_file = Path("tests/fixtures/basic_extensions.bpmn")
        definitions = parse_file(bpmn_file)

        task = definitions.processes[0].flow_elements[0]
        assert hasattr(task, 'priority')
        assert task.priority == 'high'

    def test_parse_with_defaults(self):
        """Test default values when attributes are missing."""
        bpmn_file = Path("tests/fixtures/minimal_process.bpmn")
        definitions = parse_file(bpmn_file)

        task = definitions.processes[0].flow_elements[0]
        assert task.priority == 'normal'  # Default value

    def test_invalid_attribute_raises_error(self):
        """Test that invalid attributes raise appropriate errors."""
        bpmn_file = Path("tests/fixtures/invalid_priority.bpmn")

        with pytest.raises(ValueError, match="Invalid priority"):
            parse_file(bpmn_file)

    def test_multiple_namespaces(self):
        """Test plugin handles multiple namespace prefixes."""
        bpmn_file = Path("tests/fixtures/multi_namespace.bpmn")
        definitions = parse_file(bpmn_file)

        # Verify both namespaces parsed correctly
        task = definitions.processes[0].flow_elements[0]
        assert hasattr(task, 'workflow_priority')
        assert hasattr(task, 'jira_ticket')
```

### Test with Real BPMN Files

```python
def test_with_camunda_export():
    """Test with real Camunda-exported BPMN."""
    bpmn_file = Path("tests/fixtures/camunda/sample_process.bpmn")
    definitions = parse_file(bpmn_file)

    # Verify plugin handles real-world files
    assert definitions.processes
```

### Use Fixtures

```python
@pytest.fixture
def sample_process():
    """Fixture providing a sample process."""
    bpmn_file = Path("tests/fixtures/sample.bpmn")
    definitions = parse_file(bpmn_file)
    return definitions.processes[0]

def test_with_fixture(sample_process):
    """Test using fixture."""
    assert sample_process.id
    assert len(sample_process.flow_elements) > 0
```

## Documentation

### Document All Public APIs

```python
class MyPlugin:
    """
    Plugin for custom BPMN extensions.

    This plugin adds support for custom workflow attributes including
    priority, cost estimation, and owner assignment.

    Attributes:
        name (str): Plugin name
        version (str): Plugin version
        namespaces (dict): Supported XML namespaces

    Example:
        >>> from pybpmn_parser.plugins.registry import register_plugin
        >>> plugin = MyPlugin()
        >>> register_plugin(plugin)
    """

    def parse_extension(self, element, extension_data):
        """
        Parse custom extension attributes.

        Args:
            element: The BPMN element being parsed
            extension_data: Dictionary of raw extension attributes

        Returns:
            dict: Parsed extension data with the following keys:
                - priority (str): Task priority ('low', 'medium', 'high')
                - cost (float): Estimated cost in dollars
                - owner (str): Owner identifier

        Raises:
            ValueError: If priority is invalid or cost is negative

        Example:
            >>> extension_data = {'priority': 'high', 'cost': '100'}
            >>> parsed = plugin.parse_extension(element, extension_data)
            >>> parsed['priority']
            'high'
        """
        pass
```

### Include Usage Examples

```python
"""
My Custom Plugin
================

Installation:
    pip install my-bpmn-plugin

Usage:
    from pybpmn_parser.parse import parse_file
    from my_bpmn_plugin import MyPlugin
    from pybpmn_parser.plugins.registry import register_plugin

    # Register plugin
    register_plugin(MyPlugin())

    # Parse BPMN with custom extensions
    definitions = parse_file("process.bpmn")

BPMN Example:
    <definitions xmlns:custom="http://example.com/custom">
        <process id="proc1">
            <task id="task1"
                  custom:priority="high"
                  custom:cost="100.0" />
        </process>
    </definitions>
"""
```

## Performance

### Cache Expensive Operations

```python
from functools import lru_cache

class MyPlugin:
    @lru_cache(maxsize=128)
    def _parse_complex_attribute(self, attribute_value):
        """Cache results of expensive parsing operations."""
        # Complex parsing logic here
        return parsed_value
```

### Avoid Unnecessary Parsing

```python
def parse_extension(self, element, extension_data):
    """Parse only relevant attributes."""
    namespace_uri = "http://example.com/custom"

    # Quick check: skip if no relevant attributes
    if not any(namespace_uri in key for key in extension_data.keys()):
        return {}

    # Only parse if relevant attributes exist
    parsed = {}
    for key, value in extension_data.items():
        if namespace_uri in key:
            # Parse attribute
            pass

    return parsed
```

## Security

### Validate External Input

```python
def parse_extension(self, element, extension_data):
    """Parse with input validation."""
    # Validate string lengths
    owner = extension_data.get('owner', '')
    if len(owner) > 100:
        raise ValueError("Owner name too long (max 100 characters)")

    # Validate URLs
    webhook_url = extension_data.get('webhookUrl', '')
    if webhook_url:
        from urllib.parse import urlparse
        parsed_url = urlparse(webhook_url)
        if parsed_url.scheme not in ['http', 'https']:
            raise ValueError("Invalid webhook URL scheme")

    return parsed
```

### Avoid Code Injection

```python
# Good: Use safe parsing
def parse_expression(self, expression_string):
    """Safely parse expression."""
    # Use a safe expression parser
    return ast.literal_eval(expression_string)

# Avoid: Never use eval() on user input
def parse_expression_unsafe(self, expression_string):
    return eval(expression_string)  # NEVER DO THIS!
```

## Maintenance

### Keep Dependencies Minimal

```python
# Good: Minimal dependencies
# Only import what you actually need
from typing import Dict, Any
from pybpmn_parser.plugins.registry import register_plugin

# Avoid: Heavy dependencies
# import pandas  # Unless absolutely necessary
# import numpy   # Unless absolutely necessary
```

### Follow Semantic Versioning

```
1.0.0 - Initial release
1.1.0 - Add new feature (backwards compatible)
1.1.1 - Bug fix (backwards compatible)
2.0.0 - Breaking change (NOT backwards compatible)
```

### Maintain a Changelog

```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- Support for cost estimation attributes
- Validation for priority values

### Fixed
- Bug in namespace parsing for nested elements

## [1.0.0] - 2024-01-01
### Added
- Initial plugin release
- Support for priority and owner attributes
```

## Next Steps

- Review [Creating Plugins](creating.md) for implementation details
- Check [Plugin Templates](templates.md) for starting points
- Explore the [API Reference](../reference/) for plugin APIs
