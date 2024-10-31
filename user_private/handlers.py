import httpx

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from constants import START, CITY, NOT_FOUND
from cache import Cache
import config


user_router = Router()

config = config.Config()

redis_db = Cache(username=config.redis_username, password=config.redis_password,
                 host=config.redis_host, port=config.redis_port, db=config.redis_db)


@user_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply(START)


@user_router.message(Command('weather'))
async def weather_command(message: Message):
    city = ''.join(message.text[8:].split())
    if not city:
        await message.reply(CITY)
        return

    response = redis_db.get_city(city)
    if response:
        await message.answer(response)
        return
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(config.weather_api_url, params={
                'q': city,
                'appid': config.weather_api_key,
                'units': 'metric',
                'lang': 'ru',
            })

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            result = f"Погода в городе {city} равна {temp}°C.\n\nПодробности: {description}."
            redis_db.set_city(city, result)
            await message.answer(result)
        else:
            await message.answer(NOT_FOUND)
            return
