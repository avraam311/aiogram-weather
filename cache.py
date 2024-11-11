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

    def set_weather_now(self, city: str, data: dict):
        self.cache.hset(city, mapping=data)
        self.cache.expire(city, 3600)

    def get_weather_now(self, city: str):
        response = self.cache.hgetall(city)
        return response

    def set_weather_5_days(self, city: str, data: str):
        self.cache.set(city+'5', data, ex=86400)

    def get_weather_5_days(self, city: str):
        response = self.cache.get(city+'5')
        return response
