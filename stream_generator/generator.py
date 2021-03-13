from config.config import REDIS_QUEUE_NAME
from config.config import CSV_CHUNK_SIZE
from config.config import FILE_STREAM_DIRECTORY
from config.config import FILE_NAME
from db_connectors.redis_client import RedisClient
from time import sleep
import pandas as pd
from pandas.core.frame import DataFrame
import json


redis_client = RedisClient()
FILE_PATH = "/".join([FILE_STREAM_DIRECTORY, FILE_NAME])


def get_formatted_chunk_data(chunk: DataFrame, batch_number: int) -> dict:
    """
    For optimising over IO from message broker i.e. redis queue,
    we are aggregating chunks and then creating one payload/message
    for our redis queue.
    """
    return {
        "batch": batch_number,
        "headers": chunk.columns.values.tolist(),
        "events": chunk.values.tolist()
    }


def push_events_data_to_queue(events_data: dict):
    # TODO: Exception handing if message queue service i.e. redis is down
    json_encoded_data = json.dumps(events_data)
    redis_client.put_item_into_queue(json_encoded_data)


def main():
    """
    In stream generator process, there are following steps involved
    Step 1: Create chunks from the file
    Step 2: Iterate over one chunk at a time
    Step 3: Push the data along with chunk in redis queue
    Step 4: Clean up processes
    """
    batch_number = 1
    print("Processing File:", FILE_PATH)
    for chunk in pd.read_csv(FILE_PATH, chunksize=CSV_CHUNK_SIZE):
        events_data = get_formatted_chunk_data(chunk, batch_number)
        # Pushing data to message queue
        push_events_data_to_queue(events_data)
        print(f"Batch Nr. {batch_number} : Sent to the Queue")
        batch_number += 1


if __name__ == "__main__":
    while True:
        main()
        sleep(10)
