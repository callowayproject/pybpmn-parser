"""Used to regenerate the expected output for testing the bpmn parser."""

import json
from pathlib import Path

from pybpmn_parser.core import dataclass_to_dict

repo_path = Path(__file__).parent.parent
fixtures_path = repo_path / "tests/fixtures"


def generate_expected_output() -> None:
    """Convert bpmn output to JSON."""
    from pybpmn_parser.parse import Parser

    parser = Parser()
    for filename in fixtures_path.glob("**/*.bpmn"):
        o = parser.parse_file(filename)
        output_file = filename.with_suffix(".json")
        data = dataclass_to_dict(o, skip_empty=True)
        output_file.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    print("Finished generating expected output for all fixtures.")


if __name__ == "__main__":
    generate_expected_output()
