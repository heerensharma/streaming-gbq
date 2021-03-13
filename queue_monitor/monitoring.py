from db_connectors.redis_client import RedisClient
from config.config import QUEUE_LIMIT
from time import sleep


redis_client = RedisClient()


def check_queue_size(current_queue_size: int) -> str:
    """ Checks if messages are piling up in queue which indicates two scenarios
        1. Stream Processor(s) are misbehaving
        2. Sudden burst in messages which demands processors' scaling
    """
    if current_queue_size > QUEUE_LIMIT:
        return f"ALERT: QUEUE FILLING UP -> {current_queue_size}"
    else:
        return "Queue health checks passed"


def main():
    """
    This is a very simple monitoring script.
    It checks if there are messages pending to process in our queue
    based on config variable `QUEUE_LIMIT`
    Ideally, such monitoring checks and info should be send to monitoring
    and alerting dashboards.
    """
    current_queue_size = redis_client.get_queue_size()
    # TODO: Based on use case generate and handle appropriate output
    print(check_queue_size(current_queue_size))


if __name__ == "__main__":
    while True:
        main()
        sleep(10)
