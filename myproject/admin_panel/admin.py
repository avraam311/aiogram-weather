from django.contrib import admin
from .models import UserCity


class UserCityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'city')

    def user_id(self, obj):
        return obj['user_id']

    def city(self, obj):
        return obj['city']


admin.site.register(UserCityAdmin)
