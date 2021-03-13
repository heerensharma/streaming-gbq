from stream_processor.processor import get_formatted_rows
import json


def test_get_formatted_rows():
    """
    Unit test for testing correct data and two types of expected errors
    """
    correct_data = {
        "batch": 1,
        "events": [
            ["timestamp1", json.dumps({"key1": "value1"})],
            ["timestamp2", json.dumps({"key2": "value2"})]
        ]   
    }
    fail_data_1 = {
        "events": [
            json.dumps({"key1": "value1"}),
            json.dumps({"key2": "value2"})
        ]
    }
    fail_data_2 = {
        "batch": 1,
        "events": [
            ["timestamp1", "{wrongly_formatted_json"],
            ["timestamp2", json.dumps({"key2": "value2"})]
        ]
    }
    assert get_formatted_rows(correct_data) == [
        {"key1": "value1"},
        {"key2": "value2"}
    ]
    assert get_formatted_rows(fail_data_1) == []
    assert get_formatted_rows(fail_data_2) == []
