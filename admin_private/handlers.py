# from django.conf import settings
# from myproject.admin_panel.models import WeatherAPIKey, City

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from common.filters import IsAdmin


admin_router = Router()
# admin_router.message.filter(IsAdmin())
#
#
# @admin_router.message(Command('admin'))
# async def admin_command(message: Message):
#     await message.reply("Admin panel. Use /set_api_key to set API key.")
#
#
# @admin_router.message(Command('set_api_key'))
# async def set_api_key(message: Message):
#     # Логика для установки API ключа
#     await message.reply("Please send me the new API key.")
#
#
# @admin_router.message(lambda message: True, state="*")
# async def handle_api_key(message: Message, state: FSMContext):
#     # Сохранение API ключа в базе данных
#     WeatherAPIKey.objects.update_or_create(defaults={'key': message.text})
#     await message.reply("API key has been updated.")
#     await state.finish()
