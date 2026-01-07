---
title: PyBPMN Parser
summary: Parse and validate BPMN 2.0 files in Python with type-safe dataclasses
date: 2025-09-15T12:32:13.355904+00:00
---

# PyBPMN Parser

> *A Python library for parsing and validating BPMN 2.0 files with type-safe dataclasses*

PyBPMN Parser is a powerful, extensible library that transforms BPMN XML documents into structured Python objects, making it easy to work with business process models programmatically.

## Key Features

- **Type-Safe Parsing** - Convert BPMN XML into typed Python dataclasses
- **Schema Validation** - Validate documents against the BPMN 2.0 specification
- **Vendor Extensions** - Built-in support for Moddle-based plugins
- **Easy Navigation** - Intuitive API for traversing process elements
- **Full Coverage** - Support for all BPMN 2.0 elements and attributes

## Quick Example

```python
from pathlib import Path
from pybpmn_parser.parse import Parser

# Parse a BPMN file
parser = Parser()
definitions = parser.parse_file(Path("my_process.bpmn"))

# Access process elements
for process in definitions.processes:
    print(f"Process: {process.id}")
    for element in process.flow_elements:
        print(f"  - {element.__class__.__name__}: {element.id}")
```

## Installation

Install PyBPMN Parser using pip or uv:

```bash
pip install pybpmn-parser
```

Or with uv:

```bash
uv add pybpmn-parser
```

See the [Installation Guide](installation.md) for more options.

## Documentation Sections

### Getting Started
- **[Installation](installation.md)** - Install PyBPMN Parser
- **[Quick Start](quickstart.md)** - Get up and running in minutes

### Learning
- **[Tutorials](tutorials/index.md)** - Step-by-step guides for common tasks
- **[How-Tos](howtos/index.md)** - Solutions to specific problems

### Reference
- **[API Reference](reference/api/)** - Complete API documentation
- **[Architecture](architecture/index.md)** - System design and internals

### Extending
- **[Development Guide](development.md)** - Contributing to PyBPMN Parser

## Use Cases

PyBPMN Parser is ideal for:

- **Process Analysis** - Extract metrics and insights from BPMN models
- **Model Transformation** - Convert BPMN to other formats
- **Validation Tools** - Build custom validation rules
- **Process Execution** - Power BPMN workflow engines
- **Documentation** - Generate process documentation automatically

## What Next?

- **New to PyBPMN Parser?** Start with the [Quick Start](quickstart.md) tutorial
- **Ready to dive deeper?** Explore the [Tutorials](tutorials/index.md)
- **Contributing?** See the [Developer Guide](development.md)
