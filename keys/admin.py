from django.contrib import admin
from keys.models import AvailableKeys, UsedKeys, AllKeys

# Register your models here.
admin.site.register(AvailableKeys)
admin.site.register(UsedKeys)
admin.site.register(AllKeys)
