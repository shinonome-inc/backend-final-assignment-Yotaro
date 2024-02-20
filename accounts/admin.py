from django.contrib import admin

from .models import Connection, User

admin.site.register(User)
admin.site.register(Connection)
