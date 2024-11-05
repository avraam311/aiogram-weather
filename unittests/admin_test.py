# import unittest
# from unittest.mock import AsyncMock, patch
# import redis
# from my_bot import bot, redis_client
# from django.test import TestCase
# from my_admin import AdminPanel
#
#
# # Тестирование админки на Django
# class TestAdminPanel(TestCase):
#     def setUp(self):
#         # Установка клиента Redis перед каждым тестом
#         self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
#
#     def test_admin_add_user_city(self):
#         # Попробуем добавить пользователя и город в Redis через админку
#         AdminPanel.add_user_city(123456, 'Москва')
#
#         # Проверяем, что город добавлен
#         user_city = self.redis_client.get('123456')
#         self.assertEqual(user_city.decode('utf-8'), 'Москва')
#
#     def test_admin_update_weather_info(self):
#         # Добавление информации о погоде для города
#         self.redis_client.set('Москва', 'Чисто, 15°C')
#
#         # Обновление информации о погоде в админке
#         AdminPanel.update_weather_info('Москва', 'Дождь, 10°C')
#
#         # Проверяем обновленную информацию
#         updated_weather_info = self.redis_client.get('Москва')
#         self.assertEqual(updated_weather_info.decode('utf-8'), 'Дождь, 10°C')
#
# if __name__ == '__main__':
#     unittest.main()
