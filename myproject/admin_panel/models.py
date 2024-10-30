from django.db import models


class BotSettings(models.Model):
    weather_api_key = models.CharField(max_length=255)

    def __str__(self):
        return f"Bot settings"
