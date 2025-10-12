# Exclusive Gateway Example

This example demonstrates parsing a BPMN process with exclusive gateways (decision points) using the MIWG test suite file A.4.1.bpmn.

## Overview

Exclusive gateways represent decision points where only one outgoing path is taken based on conditions. They implement conditional branching in BPMN processes.

## BPMN Pattern

This example uses the MIWG test file `A.4.1.bpmn` which demonstrates conditional decision making.

## Python Code

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

# Parse the BPMN file
bpmn_file = Path("tests/fixtures/miwg-test-suite-2025/A.4.1.bpmn")
definitions = parse_file(bpmn_file)

# Access the process
process = definitions.processes[0]
print(f"Process: {process.id}")
print(f"Name: {process.name}")

# Find exclusive gateways
exclusive_gateways = [
    el for el in process.flow_elements
    if isinstance(el, ExclusiveGateway)
]

print(f"\nFound {len(exclusive_gateways)} exclusive gateway(s)")

for gw in exclusive_gateways:
    print(f"\nGateway: {gw.id}")
    print(f"  Name: {gw.name}")

    # Check for default flow
    if hasattr(gw, 'default') and gw.default:
        print(f"  Default flow: {gw.default}")

    # Find outgoing flows
    outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]
    print(f"  Outgoing paths: {len(outgoing)}")

    for flow in outgoing:
        flow_info = f"    To: {flow.target_ref}"
        if flow.name:
            flow_info += f" ({flow.name})"
        if hasattr(flow, 'condition_expression') and flow.condition_expression:
            flow_info += " [conditional]"
        print(flow_info)
```

## Understanding Exclusive Gateways

### Decision Points

Exclusive gateways evaluate conditions to determine which path to follow:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.4.1.bpmn"))
process = definitions.processes[0]

def analyze_decision_points(process):
    """Analyze decision complexity."""
    exclusive_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ExclusiveGateway)
    ]

    decisions = []
    for gw in exclusive_gateways:
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]

        # Only split gateways are decision points
        if len(outgoing) > 1:
            decisions.append({
                'gateway': gw.id,
                'name': gw.name,
                'options': len(outgoing),
                'has_default': hasattr(gw, 'default') and gw.default is not None
            })

    return decisions

decisions = analyze_decision_points(process)
print("Decision Points:")
for decision in decisions:
    print(f"\n{decision['name']} ({decision['gateway']})")
    print(f"  Options: {decision['options']}")
    print(f"  Has default: {decision['has_default']}")
```

### Conditional Flows

Sequence flows from exclusive gateways may have conditions:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.4.1.bpmn"))
process = definitions.processes[0]

def extract_conditions(process):
    """Extract condition information from flows."""
    exclusive_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ExclusiveGateway)
    ]

    conditions = []
    for gw in exclusive_gateways:
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]

        for flow in outgoing:
            condition_info = {
                'from_gateway': gw.id,
                'flow_id': flow.id,
                'flow_name': flow.name,
                'target': flow.target_ref,
                'has_condition': False,
                'is_default': False
            }

            # Check if this is the default flow
            if hasattr(gw, 'default') and gw.default == flow.id:
                condition_info['is_default'] = True

            # Check for condition expression
            if hasattr(flow, 'condition_expression') and flow.condition_expression:
                condition_info['has_condition'] = True

            conditions.append(condition_info)

    return conditions

conditions = extract_conditions(process)
print("Flow Conditions:")
for cond in conditions:
    flow_type = "default" if cond['is_default'] else "conditional" if cond['has_condition'] else "unconditional"
    print(f"\n{cond['flow_name']} ({cond['flow_id']}) [{flow_type}]")
    print(f"  From: {cond['from_gateway']}")
    print(f"  To: {cond['target']}")
```

## Merge Gateways

Exclusive gateways can also merge flows:

```python
from pathlib import Path
from pybpmn_parser.parse import parse_file
from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.4.1.bpmn"))
process = definitions.processes[0]

def classify_gateways(process):
    """Classify gateways as split, merge, or both."""
    exclusive_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ExclusiveGateway)
    ]

    classified = []
    for gw in exclusive_gateways:
        incoming = [f for f in process.sequence_flows if f.target_ref == gw.id]
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]

        gateway_type = "unknown"
        if len(incoming) == 1 and len(outgoing) > 1:
            gateway_type = "split"
        elif len(incoming) > 1 and len(outgoing) == 1:
            gateway_type = "merge"
        elif len(incoming) > 1 and len(outgoing) > 1:
            gateway_type = "mixed"

        classified.append({
            'id': gw.id,
            'name': gw.name,
            'type': gateway_type,
            'incoming': len(incoming),
            'outgoing': len(outgoing)
        })

    return classified

gateways = classify_gateways(process)
print("Gateway Classification:")
for gw in gateways:
    print(f"\n{gw['name']} ({gw['id']})")
    print(f"  Type: {gw['type']}")
    print(f"  Incoming: {gw['incoming']}, Outgoing: {gw['outgoing']}")
```

## Key Concepts

- **Decision Point**: Gateway evaluates conditions to choose a path
- **Exclusive Choice**: Only ONE outgoing path is taken
- **Default Flow**: Taken when no conditions are met
- **Merge Point**: Multiple paths converge back to one

## Common Patterns

### Simple If-Then-Else

```
Gateway -> [Condition A] -> Task A -> Merge
        -> [Default]     -> Task B ->
```

### Multiple Conditions

```
Gateway -> [Condition 1] -> Path 1
        -> [Condition 2] -> Path 2
        -> [Default]     -> Path 3
```

## Calculating Process Complexity

```python
def calculate_cyclomatic_complexity(process):
    """Calculate cyclomatic complexity of the process."""
    from pybpmn_parser.bpmn.gateways.exclusive_gateways import ExclusiveGateway
    from pybpmn_parser.bpmn.gateways.parallel_gateways import ParallelGateway

    # Cyclomatic complexity = E - N + 2P
    # Where E = edges, N = nodes, P = connected components
    # For simplicity, we count decision points

    exclusive_gateways = [
        el for el in process.flow_elements
        if isinstance(el, ExclusiveGateway)
    ]

    decision_points = 0
    for gw in exclusive_gateways:
        outgoing = [f for f in process.sequence_flows if f.source_ref == gw.id]
        if len(outgoing) > 1:
            decision_points += (len(outgoing) - 1)

    return decision_points + 1

definitions = parse_file(Path("tests/fixtures/miwg-test-suite-2025/A.4.1.bpmn"))
process = definitions.processes[0]

complexity = calculate_cyclomatic_complexity(process)
print(f"Process Cyclomatic Complexity: {complexity}")
```

## Next Steps

- Review [Sequential Flow](sequential-flow.md) for basic patterns
- Study [Parallel Gateway](parallel-gateway.md) for concurrent execution
- Explore [Working with Elements](../tutorials/elements.md) for more techniques
