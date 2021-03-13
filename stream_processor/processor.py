from time import sleep
from typing import List
import json
from json import JSONDecodeError
from db_connectors.redis_client import RedisClient
from db_connectors.gbq_client import GBQClient
from config.config import SLEEP_TIMEOUT

redis_client = RedisClient()
gbq_client = GBQClient()


def get_queue_item():
    return redis_client.get_item_from_queue(json_flag=True)


def get_formatted_rows(raw_records: dict) -> List[dict]:
    """
    Take events from queue item and convert them into format
    [
        {event_1},
        {event_2}
    ]
    :params:
        - raw_records : data stream entry have format
                        {"events": list, "batch": int, "headers": list}
                        and `events` key holds batch of events
    """
    # TODO: Check of incoming data quality. We should check message format and if required types
    # corresponding a schema registry.
    # Ideally one can raise hard exception or fail softly. Former one might be preferred based
    # on SLAs and quality policies.
    try:
        print("Processing Batch:", raw_records["batch"])
        rows = list(map(lambda record: json.loads(record[1]), raw_records["events"]))
        return rows
    except JSONDecodeError:
        print("ERROR: One or more records are not in correct JSON encoded format.")
    except KeyError:
        print("ERROR: `events` or `batch` key not present in input records data")
    
    # Failing softly
    return []


def main():
    """
    In stream processor process, following steps are involved
    Step 1: Take out item from queue
    Step 2: Format the records
    Step 3: Send request to Bigquery to insert results into table
    """
    # TODO: In case of process failure, we should gracefully put the unprocessed
    # message back to redis queue.
    raw_records = get_queue_item()
    if raw_records:
        rows_to_insert = get_formatted_rows(raw_records)
        print("Number of Rows Extracted:", len(rows_to_insert))
        gbq_client.insert_rows_in_table(
            "test_project.test_dataset.test_table", rows_to_insert
        )
    else:
        print("No records to fetch as queue is empty")
        print(f"Sleeping for {SLEEP_TIMEOUT} seconds")
        sleep(SLEEP_TIMEOUT)


if __name__ == "__main__":
    while True:
        main()
