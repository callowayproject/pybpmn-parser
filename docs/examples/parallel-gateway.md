# Parallel Gateway Example

This example demonstrates parsing a BPMN process with parallel gateways using the MIWG test suite file A.2.0.bpmn.

## Overview

Parallel gateways split the process flow into multiple concurrent paths that execute simultaneously, then synchronize at a join gateway.

## BPMN Pattern

This example uses the MIWG test file `A.2.0.bpmn` which demonstrates parallel execution.

## Python Code

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

# Parse the BPMN file
bpmn_file = Path("tests/fixtures/miwg-test-suite-2025/A.2.0.bpmn")
definitions = parse_file(bpmn_file)

# Access the process
process = definitions.processes[0]
print(f"Process: {process.id}")
print(f"Name: {process.name}")

# Find parallel gateways
parallel_gateways = [
    el for el in process.flow_elements
    if isinstance(el, ParallelGateway)
]

print(f"\nFound {len(parallel_gateways)} parallel gateway(s)")

for gw in parallel_gateways:
    print(f"\nGateway: {gw.id}")
    print(f"  Name: {gw.name}")

    # Find incoming flows (for join gateways)
    incoming = [f for f in process.sequence_flows if f.target_ref == gw.id]
    print(f"  Incoming flows: {len(incoming)}")
    for flow in incoming:
        print(f"    From: {flow.source_ref}")

    # Find outgoing flows (for split gateways)
    outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]
    print(f"  Outgoing flows: {len(outgoing)}")
    for flow in outgoing:
        print(f"    To: {flow.target_ref}")
```

## Expected Output

```
Process: _6-1
Name: A.2.0

Found 2 parallel gateway(s)

Gateway: _6-125
  Name: Fork
  Incoming flows: 1
    From: _6-74
  Outgoing flows: 2
    To: _6-178
    To: _6-420

Gateway: _6-686
  Name: Join
  Incoming flows: 2
    From: _6-178
    From: _6-420
  Outgoing flows: 1
    To: _6-748
```

## Analyzing Parallel Execution

### Identifying Parallel Branches

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.2.0.bpmn"))
process = definitions.processes[0]

def find_parallel_branches(process):
    """Find all parallel execution branches."""
    parallel_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ParallelGateway)
    ]

    branches = []
    for gw in parallel_gateways:
        # Split gateways have multiple outgoing flows
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]
        if len(outgoing) > 1:
            branches.append({
                'gateway': gw.id,
                'gateway_name': gw.name,
                'branch_count': len(outgoing),
                'branches': [f.target_ref for f in outgoing]
            })

    return branches

branches = find_parallel_branches(process)
print("Parallel Branches:")
for branch in branches:
    print(f"\n{branch['gateway_name']} ({branch['gateway']})")
    print(f"  Splits into {branch['branch_count']} branches:")
    for target in branch['branches']:
        print(f"    - {target}")
```

### Calculating Parallelism Degree

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

def calculate_max_parallelism(process):
    """Calculate maximum degree of parallelism."""
    parallel_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ParallelGateway)
    ]

    max_parallel = 1
    for gw in parallel_gateways:
        # Check outgoing flows for split gateways
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]
        if len(outgoing) > max_parallel:
            max_parallel = len(outgoing)

    return max_parallel

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.2.0.bpmn"))
process = definitions.processes[0]

max_parallel = calculate_max_parallelism(process)
print(f"Maximum parallelism degree: {max_parallel}")
```

## Key Concepts

- **Fork Gateway**: Splits flow into multiple parallel paths
- **Join Gateway**: Synchronizes parallel paths back into one
- **Concurrent Execution**: All parallel paths execute simultaneously
- **Synchronization**: Join waits for all incoming paths to complete

## Common Patterns

### Balanced Fork-Join

The most common pattern has matching fork and join gateways:

```
Fork -> [Branch 1] -> Join
     -> [Branch 2] ->
```

### Detecting Unbalanced Gateways

```python
def check_balanced_gateways(process):
    """Check if fork and join gateways are balanced."""
    from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

    parallel_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ParallelGateway)
    ]

    issues = []
    for gw in parallel_gateways:
        incoming = [f for f in process.sequence_flows if f.target_ref == gw.id]
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]

        # Fork: 1 incoming, N outgoing
        # Join: N incoming, 1 outgoing
        if len(incoming) == 1 and len(outgoing) == 1:
            issues.append(f"Gateway {gw.id} has 1-to-1 flow (unnecessary?)")
        elif len(incoming) > 1 and len(outgoing) > 1:
            issues.append(f"Gateway {gw.id} is both fork and join")

    return issues
```

## Next Steps

- Learn about [Exclusive Gateway](exclusive-gateway.md) for conditional logic
- Review [Sequential Flow](sequential-flow.md) for basic patterns
- Study [Working with Elements](../tutorials/elements.md) for navigation techniques
