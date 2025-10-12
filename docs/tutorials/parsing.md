# Parsing BPMN Files

This tutorial covers all the ways to parse BPMN documents with PyBPMN Parser.

## Overview

PyBPMN Parser provides two main functions for parsing BPMN documents:

- `parse(xml_str)` - Parse from a string
- `parse_file(xml_file)` - Parse from a file path

Both functions return a `Definitions` object representing the root of the BPMN document.

## Parsing from Files

The most common use case is parsing BPMN files from disk:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Parse a BPMN file
definitions = parse_file(Path("my_process.bpmn"))

# Access processes in the document
for process in definitions.processes:
    print(f"Found process: {process.id}")
```

### Using Relative Paths

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Current directory
definitions = parse_file(Path("process.bpmn"))

# Subdirectory
definitions = parse_file(Path("bpmn_models/order_process.bpmn"))

# Parent directory
definitions = parse_file(Path("../shared/common_process.bpmn"))
```

### Using Absolute Paths

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Absolute path
definitions = parse_file(Path("/opt/bpmn/processes/my_process.bpmn"))

# Home directory
definitions = parse_file(Path.home() / "Documents" / "bpmn" / "process.bpmn")
```

## Parsing from Strings

Parse BPMN XML directly from strings:

```python
from pybpmn_parser.parse import parse

bpmn_xml = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             targetNamespace="http://bpmn.io/schema/bpmn">
    <process id="simple_process" name="Simple Process">
        <startEvent id="start" />
        <endEvent id="end" />
    </process>
</definitions>"""

definitions = parse(bpmn_xml)
```

This is useful when:

- Loading BPMN from a database
- Receiving BPMN via HTTP API
- Generating BPMN programmatically
- Testing with inline XML

### Parsing from HTTP Responses

```python
import requests
from pybpmn_parser.parse import parse

# Fetch BPMN from a web service
response = requests.get("https://example.com/api/processes/123")
bpmn_xml = response.text

# Parse it
definitions = parse(bpmn_xml)
```

### Parsing from Database

```python
from pybpmn_parser.parse import parse

# Assuming you have a database connection
cursor = db.execute("SELECT bpmn_xml FROM processes WHERE id = ?", (process_id,))
bpmn_xml = cursor.fetchone()[0]

# Parse the stored BPMN
definitions = parse(bpmn_xml)
```

## Error Handling

PyBPMN Parser validates documents during parsing. Handle validation errors appropriately:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.validator import ValidationError

try:
    definitions = parse_file(Path("my_process.bpmn"))
    print("✓ Successfully parsed and validated")
except FileNotFoundError:
    print("✗ BPMN file not found")
except ValidationError as e:
    print(f"✗ Invalid BPMN: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
```

### Understanding Validation Errors

ValidationError exceptions contain detailed information:

```python
from pybpmn_parser.parse import parse
from pybpmn_parser.validator import ValidationError

invalid_xml = """<?xml version="1.0"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <invalidElement />
</definitions>"""

try:
    definitions = parse(invalid_xml)
except ValidationError as e:
    print("Validation failed:")
    print(f"  Message: {e}")
    # The error contains details about what went wrong
```

## Parsing Multiple Files

Process multiple BPMN files in a directory:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.validator import ValidationError

def parse_directory(directory: Path):
    """Parse all BPMN files in a directory."""
    results = {"success": [], "failed": []}

    for bpmn_file in directory.glob("*.bpmn"):
        try:
            definitions = parse_file(bpmn_file)
            results["success"].append({
                "file": bpmn_file.name,
                "processes": len(definitions.processes)
            })
        except ValidationError as e:
            results["failed"].append({
                "file": bpmn_file.name,
                "error": str(e)
            })

    return results

# Parse all BPMN files
results = parse_directory(Path("bpmn_models/"))

print(f"Successfully parsed: {len(results['success'])} files")
print(f"Failed to parse: {len(results['failed'])} files")

for item in results["failed"]:
    print(f"  {item['file']}: {item['error']}")
```

## Accessing the Definitions Object

The `Definitions` object is the root of every BPMN document:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("my_process.bpmn"))

# Document metadata
print(f"Target Namespace: {definitions.target_namespace}")
print(f"Exporter: {definitions.exporter}")
print(f"Exporter Version: {definitions.exporter_version}")

# Processes
print(f"\nProcesses: {len(definitions.processes)}")
for process in definitions.processes:
    print(f"  - {process.id}: {process.name}")

# Collaborations (if present)
if definitions.collaborations:
    print(f"\nCollaborations: {len(definitions.collaborations)}")
```

## Parsing BPMN with Collaborations

BPMN files can contain collaborations (pools and lanes):

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

definitions = parse_file(Path("collaboration_process.bpmn"))

# Access collaborations
for collaboration in definitions.collaborations:
    print(f"Collaboration: {collaboration.id}")

    # Access participants (pools)
    for participant in collaboration.participants:
        print(f"  Participant: {participant.name}")
        # Each participant references a process
        process_ref = participant.process_ref
        print(f"    Process Ref: {process_ref}")
```

## Performance Considerations

### Caching Parsed Results

For files you parse repeatedly, consider caching:

```python
from pathlib import Path
from functools import lru_cache
from pybpmn_parser.parse import parse_file

@lru_cache(maxsize=100)
def cached_parse(file_path: str):
    """Parse and cache BPMN files."""
    return parse_file(Path(file_path))

# First call parses the file
definitions1 = cached_parse("my_process.bpmn")

# Second call returns cached result
definitions2 = cached_parse("my_process.bpmn")
```

### Memory Usage

For very large BPMN files (> 10MB), parse in a context where memory can be freed:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

def process_large_file(file_path: Path):
    """Process a large BPMN file and extract summary."""
    definitions = parse_file(file_path)

    # Extract only what you need
    summary = {
        "process_count": len(definitions.processes),
        "process_ids": [p.id for p in definitions.processes]
    }

    # definitions will be garbage collected after this function returns
    return summary

# Use the extracted summary instead of keeping the full object
summary = process_large_file(Path("large_process.bpmn"))
```

## Best Practices

### Always Use Path Objects

Use `pathlib.Path` instead of strings:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

# Good: Use Path objects
definitions = parse_file(Path("my_process.bpmn"))

# Avoid: Using string paths directly
# definitions = parse_file("my_process.bpmn")  # This still works but is less robust
```

### Validate Before Processing

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.validator import ValidationError

def safe_parse(file_path: Path):
    """Parse with proper error handling."""
    try:
        definitions = parse_file(file_path)
        return definitions, None
    except ValidationError as e:
        return None, f"Validation error: {e}"
    except FileNotFoundError:
        return None, "File not found"
    except Exception as e:
        return None, f"Unexpected error: {e}"

# Use the safe parser
definitions, error = safe_parse(Path("my_process.bpmn"))
if error:
    print(f"Failed to parse: {error}")
else:
    print("Successfully parsed!")
```

### Check File Existence

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file

file_path = Path("my_process.bpmn")

if not file_path.exists():
    print(f"File does not exist: {file_path}")
elif not file_path.is_file():
    print(f"Path is not a file: {file_path}")
else:
    definitions = parse_file(file_path)
```

## Next Steps

- Learn how to navigate BPMN elements in [Working with Elements](elements.md)
- Understand validation in detail in [Validating Documents](validation.md)
- See real examples in the [Examples Gallery](../examples/index.md)
