# Data source specific configuration
## Based on https://cloud.google.com/bigquery/quotas#streaming_inserts
CSV_CHUNK_SIZE = 500
FILE_STREAM_DIRECTORY = "/main_data_bucket"  # volume mount location inside container
FILE_NAME = "data_source.csv"

# Redis specific config values
REDIS_QUEUE_NAME = "FILE_CHUNK_QUEUE"

# Stream processor config values
SLEEP_TIMEOUT = 10  # in seconds

# Monitoring processor
QUEUE_LIMIT = 100  # If queue fills up above it, alarm should be raised
