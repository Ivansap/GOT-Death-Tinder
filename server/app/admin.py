from django.contrib import admin
from .models import *

# from fcm_django.models import FCMDevice

admin.site.register(CardAnswer)
admin.site.register(User)
admin.site.register(UserAnswer)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'showtime', 'number', 'status')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'question', 'series', 'character')

