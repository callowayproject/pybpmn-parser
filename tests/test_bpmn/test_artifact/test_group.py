"""Test the Group class."""

import pytest

from pybpmn_parser.bpmn.common.group import Group
from tests._utils import example_tags, get_params, xml_test

params = get_params(example_tags()["group"])


@pytest.mark.parametrize(
    ["xml", "expected"],
    params,
)
def test_parse_group(xml: str, expected: dict):
    """Test parsing a Group object."""
    xml_test(xml, expected, "bpmn:group", Group)
