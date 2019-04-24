from django.contrib import admin
from .models import *

from fcm_django.models import FCMDevice

# Register your models here.
admin.site.register(Series)
admin.site.register(Character)
admin.site.register(Card)
admin.site.register(CardAnswer)
admin.site.register(User)
admin.site.register(UserAnswer)

