# Working with BPMN Extensions

This tutorial covers how to work with vendor-specific BPMN extensions in PyBPMN Parser.

## BPMN Extensions

The BPMN spec defines the ability to add vendor-specific extensions to elements.
Vendors are allowed to extend attributes of elements and add new elements.
PyBPMN Parser supports all vendor extensions, regardless of whether it recognizes them or not.

We start with parsing the C.1.1 BPMN file of the MIWG Test Suite:

```python
from pathlib import Path
from pybpmn_parser.parse import Parser

parser = Parser()
bpmn_path = Path("tests/fixtures/miwg-test-suite-2025/C.1.1.bpmn")
definition = parser.parse_file(bpmn_path)
```

## Extension Attributes

Extension attributes are stored as attributes of the element they're attached to.
Their names, with the vendor prefix, are converted to snake case.

```xml
<serviceTask id="archiveInvoice"
             camunda:delegateExpression="#{archiveService}"
             w4:serviceName="ArchiveInvoiceService"
             name="Archive&#xA;Invoice"
             completionQuantity="1"
             isForCompensation="false"
             startQuantity="1"
             implementation="##unspecified"
></serviceTask>
```

We can access the `delegateExpression` attribute in the `camunda` namespace with the name `camunda_delegate_expression`:

```python
print(definition.processes[0].service_tasks[0].camunda_delegate_expression)
# #{archiveService}
```

We can access the `serviceName` attribute in the `w4` namespace with the name `w_4_service_name`:

```python
print(definition.processes[0].service_tasks[0].w_4_service_name)
# ArchiveInvoiceService
```

## Extension Elements

Extension Elements are stored as attributes of the `extension_elements` class.
Recognized extensions are converted to a dataclass with the appropriate data types.
If the extension is not recognized, it is stored as a dictionary.

```python
type(definition.processes[0].service_tasks[0].extension_elements.camunda_field[0])
# <class 'pybpmn_parser.plugins.moddle.Field'>

type(definition.processes[0].service_tasks[0].extension_elements.signavio_signavio_meta_data[0])
# <class 'dict'>
```

Since `camunda` is a recognized extension, PyBPMN Parser converts this XML:

```xml
<camunda:field name="text0" stringValue="Hello World"/>
```

To this Python object:

```python
@dataclass
class Field:
    name: str
    string_value: str

Field(name="text0", string_value="Hello World")
```

The `signavio` extension is not recognized by PyBPMN Parser, so PyBPMN Parser converts this XML:

```xml
<signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffcc"/>
```

To this Python object:

```python
{'@metaKey': 'bgcolor', '@metaValue': '#ffffcc'}
```

The dictionary is created using the [xmltodict](https://xmltodict.readthedocs.io/en/stable/README/) library.
