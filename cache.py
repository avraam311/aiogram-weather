import redis


class Cache:
    def __init__(self, username: str, password: str, host: str, port: int, db: int):
        self.cache = redis.Redis(username=username, password=password,
                                 host=host, port=port, db=db,
                                 decode_responses=True)

    def set_city(self, user_id: int, city: str):
        self.cache.set(str(user_id), city)

    def get_city(self, user_id: int):
        response = self.cache.get(str(user_id))
        return response
