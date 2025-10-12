"""Test the TextAnnotation class."""

import pytest

from pybpmn_parser.bpmn.common.text_annotation import TextAnnotation
from tests._utils import example_tags, get_params, xml_test

params = get_params(example_tags()["text_annotation"])


@pytest.mark.parametrize(
    ["xml", "expected"],
    params,
)
def test_parse_text_annotation(xml: str, expected: dict):
    """Test parsing a TextAnnotation object without text."""
    xml_test(xml, expected, "bpmn:textAnnotation", TextAnnotation)
