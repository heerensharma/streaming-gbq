from stream_generator.generator import get_formatted_chunk_data
import pandas as pd


def test_get_formatted_chunk_data():
    test_df = pd.DataFrame.from_dict(
        {
            "event_date": ["timestamp1", "timestamp2"],
            "records": [{"name": "event1"}, {"name": "event2"}]
        }
    )
    formatted_chunk_data = get_formatted_chunk_data(chunk=test_df, batch_number=1)
    assert formatted_chunk_data == {
        "batch": 1,
        "headers": ["event_date", "records"],
        "events": [["timestamp1", {"name": "event1"}], ["timestamp2", {"name": "event2"}]]
    }
