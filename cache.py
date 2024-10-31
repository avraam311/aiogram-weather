import redis


class Cache:
    def __init__(self, username: str, password: str, host: str, port: int, db: int):
        self.cache = redis.Redis(username=username, password=password,
                                 host=host, port=port, db=db,
                                 decode_responses=True)

    def set_city(self, city: str, info: str):
        self.cache.set(city, info, ex=3600)

    def get_city(self, city: str):
        response = self.cache.get(city)
        return response
