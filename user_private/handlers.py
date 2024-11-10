import httpx

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from user_private import keyboards as kb
from constants import CITY, NOT_FOUND, NOT_SET
from cache import Cache
import config


user_router = Router()

config = config.Config()

redis_db = Cache(username=config.redis_username, password=config.redis_password,
                 host=config.redis_host, port=config.redis_port, db=config.redis_db)


# FSM машина для указания города########################
class Weather(StatesGroup):
    set_city = State()
    change_city = State()


@user_router.message(StateFilter(None), F.text == "Указать город")
@user_router.message(StateFilter(None), CommandStart())
async def f_city(message: Message, state: FSMContext):
    await message.reply(CITY,
                        reply_markup=kb.cancel)
    await state.set_state(Weather.set_city)
    

@user_router.message(Weather.set_city, F.text == 'Отмена')
async def city_cancel(message: Message, state: FSMContext):
    await message.answer(message.text, reply_markup=kb.city)
    await state.clear()


@user_router.message(Weather.set_city, F.text)
async def add_city(message: Message, state: FSMContext):
    city = message.text
    user_id = message.from_user.id
    redis_db.set_city(user_id, city)
    async with httpx.AsyncClient() as client:
        response_a_day = await client.get(config.weather_api_url, params={
            'q': city,
            'appid': config.weather_api_key,
            'units': 'metric',
            'lang': 'ru',
        })
        if response_a_day.status_code == 200:
            data = response_a_day.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            result = f"Погода в городе {city} равна {temp}°C.\n\nПодробности: {description}."
            await message.answer(result,
                                 reply_markup=kb.weather)
            await state.clear()
        else:
            await message.answer(NOT_FOUND)


# ловим некоррекный ввод
@user_router.message(Weather.set_city)
async def error(message: Message):
    await message.answer("Введите название города или нажмите \"Отмена\"",
                         reply_markup=kb.cancel)
################################


# FSM машина для изменения города########################
@user_router.message(StateFilter(None), F.text == "Поменять город")
@user_router.message(StateFilter(None), Command('city'))
async def f_city(message: Message, state: FSMContext):
    await message.reply(CITY,
                        reply_markup=kb.cancel)
    await state.set_state(Weather.change_city)


@user_router.message(Weather.change_city, F.text == 'Отмена')
async def city_cancel(message: Message, state: FSMContext):
    await message.answer(message.text, reply_markup=kb.weather)
    await state.clear()


@user_router.message(Weather.change_city, F.text)
async def add_city(message: Message, state: FSMContext):
    city = message.text
    user_id = message.from_user.id
    redis_db.set_city(user_id, city)
    async with httpx.AsyncClient() as client:
        response_a_day = await client.get(config.weather_api_url, params={
            'q': city,
            'appid': config.weather_api_key,
            'units': 'metric',
            'lang': 'ru',
        })
        if response_a_day.status_code == 200:
            data = response_a_day.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            result = f"Погода в городе {city} равна {temp}°C.\n\nПодробности: {description}."
            await message.answer(result,
                                 reply_markup=kb.weather)
            await state.clear()
            return
        else:
            await message.answer(NOT_FOUND)
            return


# ловим некоррекный ввод
@user_router.message(Weather.change_city)
async def error(message: Message):
    await message.answer("Введите название города или нажмите \"Отмена\"",
                         reply_markup=kb.cancel)
################################


@user_router.message(F.text == "Погода сейчас")
@user_router.message(Command('weather_now'))
async def f_weather_now(message: Message):
    city = redis_db.get_city(message.from_user.id)

    if not city:
        await message.answer(NOT_SET)
        return

    async with httpx.AsyncClient() as client:
        response_a_day = await client.get(config.weather_api_url, params={
            'q': city,
            'appid': config.weather_api_key,
            'units': 'metric',
            'lang': 'ru',
        })
        if response_a_day.status_code == 200:
            data = response_a_day.json()
            await message.answer(str(data),
                                 reply_markup=kb.weather)
        else:
            await message.answer(NOT_FOUND)


@user_router.message(F.text == "Погода на 5 дней")
@user_router.message(Command('weather_5_days'))
async def f_weather_5_days(message: Message):
    city = redis_db.get_city(message.from_user.id)

    if not city:
        await message.answer(NOT_SET)
        return

    async with httpx.AsyncClient() as client:
        response_a_day = await client.get(config.forecast_api_url, params={
            'q': city,
            'appid': config.weather_api_key,
            'units': 'metric',
            'lang': 'ru',
            'cnt': 40,
        })
        if response_a_day.status_code == 200:
            data = response_a_day.json()
            days = ("Сегодня", "Завтра", "Послезавтра", "На 4-й день", "На 5-й день")
            for i in range(5):
                forecast_days = data['list']
                await message.answer(f"{days[i]}: \n\n"
                                     f"Температура: {forecast_days[i]['main']['temp']} °C, \n"
                                     f"Ощущается: {forecast_days[i]['main']['feels_like']} °C, \n"
                                     f"Влажность: {forecast_days[i]['main']['humidity']} г/м³, \n"
                                     f"Погода: {forecast_days[i]['weather'][0]['main']}, \n"
                                     f"Подробности: {forecast_days[i]['weather'][0]['description']}, \n"
                                     f"Скорость ветра: {forecast_days[i]['wind']['speed']}м/с.",
                                     reply_markup=kb.weather)
        else:
            await message.answer(NOT_FOUND)
