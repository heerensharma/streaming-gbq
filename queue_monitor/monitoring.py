from db_connectors.redis_client import RedisClient
from config.config import QUEUE_LIMIT
from time import sleep


redis_client = RedisClient()


def main():
    """
    This is a very simple monitoring script.
    It checks if there are messages pending to process in our queue
    based on config variable `QUEUE_LIMIT`
    Ideally, such monitoring checks and info should be send to monitoring
    and alerting dashboards.
    """
    current_queue_size = redis_client.get_queue_size()
    if current_queue_size > QUEUE_LIMIT:
        print("ALERT: QUEUE FILLING UP ->", current_queue_size)
    else:
        print("Queue health checks passed")


if __name__ == "__main__":
    while True:
        main()
        sleep(10)
