import unittest
from unittest.mock import AsyncMock, patch
from user_private import handlers


# Тестирование телеграм бота
class TestWeatherBot(unittest.TestCase):
    @patch('aiogram.Bot.get_updates', new_callable=AsyncMock)
    async def test_get_weather(self, mock_get_updates):
        # Имитация ответа от пользователя с текстом запроса
        mock_get_updates.return_value = [
            {'message': {'from': {'id': 123456}, 'text': 'Москва'}}
        ]

        # Вызов функции получения погоды
        await handlers.f_weather_now(123456, 'Москва')

        # Проверяем, что город был сохранён в Redis для данного пользователя
        user_city = await handlers.redis_db.get('123456')
        self.assertEqual(user_city, 'Москва')

        # Здесь мы также проверим, что информация о погоде сохранена
        expected_weather_info = 'Температура в Москве: 15°C'  # Пример ожидаемого ответа
        actual_weather_info = await handlers.redis_db.get('Москва')
        self.assertEqual(actual_weather_info, expected_weather_info)


if __name__ == '__main__':
    unittest.main()
