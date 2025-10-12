# Examples Gallery

This section provides practical examples using real BPMN files from the MIWG (Model Interchange Working Group) test suite. Each example includes complete Python code, explanations, and expected outputs.

## Available Examples

### Basic Process Patterns

- **[Sequential Flow](sequential-flow.md)** - Simple sequential process with linear task execution
- **[Parallel Gateway](parallel-gateway.md)** - Parallel execution paths with synchronization
- **[Exclusive Gateway](exclusive-gateway.md)** - Conditional branching and decision points

## About MIWG Test Suite

The examples use BPMN files from the [MIWG test suite](https://github.com/bpmn-miwg/bpmn-miwg-test-suite), which provides standardized BPMN models for testing interoperability between BPMN tools.

## How to Use These Examples

Each example includes:

1. **Overview** - Description of the BPMN pattern
2. **BPMN File** - Reference to the test file used
3. **Complete Code** - Full Python implementation
4. **Output** - Expected results when running the code
5. **Variations** - Common modifications and use cases

## Running the Examples

All examples can be run directly after installing PyBPMN Parser:

```bash
pip install pybpmn-parser
```

Download the example BPMN files from the `tests/fixtures/miwg-test-suite-2025/` directory in the repository.

## Next Steps

Start with the [Sequential Flow](sequential-flow.md) example to learn the basics, then explore more complex patterns.
