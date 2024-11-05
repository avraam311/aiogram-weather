import redis
from django.conf import settings
from cache import Cache
import config

config = config.Config()


class UserCity:
    def __init__(self):
        self.redis_client = redis.Redis(username=config.redis_username, password=config.redis_password,
                                        host=config.redis_host, port=config.redis_port, db=config.redis_db)

    def set_city(self, user_id, city):
        self.redis_client.set(user_id, city)

    def get_city(self, user_id):
        return self.redis_client.get(user_id)

    def delete_city(self, user_id):
        self.redis_client.delete(user_id)
