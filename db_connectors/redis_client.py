import redis
from typing import Any
import json
import os
from config.config import REDIS_QUEUE_NAME


REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = os.getenv("REDIS_PORT", 6379)


class RedisClient:
    """
    This is a wrapper for redis client which connects to a redis server
    and specifically programmed APIs for using redis as queue.
    """
    def __init__(self):
        # Initialising Redis client
        # TODO: In case we need to use multiple redis client objects
        # then we need to create a singleton class so as not to
        # initialize a new redis connection to server instead of reusing
        # same connection or from a pool of connections
        self.__db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def get_key(self, key_name: str) -> str:
        """ Get specific key """
        return self.__db.get(key_name)

    def set_key(self, key_name: str, key_value: Any) -> str:
        """ Set specific key 
        :params
            - key_name :  redis key
            - key_value : value to assign to that key
        """
        return self.__db.set(key_name, key_value)

    def get_item_from_queue(self, json_flag: bool = False) -> str:
        """Remove and return an item from the queue.
        It will return None if no items are present in list
        :params
            - json_flag : If True, it serializes record into json object
        """
        # TODO: We can enhance by putting blocking pop
        # Might be useful in distributed environment
        # item = self.__db.blpop(REDIS_QUEUE_NAME, timeout=timeout)
        item = self.__db.lpop(REDIS_QUEUE_NAME)
        if json_flag and item:
            return json.loads(item)
        return item

    def put_item_into_queue(self, item: Any):
        """ Putting item into queue """
        self.__db.rpush(REDIS_QUEUE_NAME, item)

    def get_queue_size(self) -> int:
        """ Get redis queue size """
        return self.__db.llen(REDIS_QUEUE_NAME)

    def is_queue_empty(self) -> bool:
        """ This will return True if there are 0 items in queue otherwise False """
        return self.get_queue_size() == 0
